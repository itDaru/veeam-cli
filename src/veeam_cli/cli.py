
import click
import json
import csv
import sys
from rich.console import Console
from rich.table import Table
from .client import VeeamApiClient

@click.group()
def cli():
    """A CLI for interacting with the Veeam Backup & Replication API."""
    pass

@cli.group()
def jobs():
    """Manage backup jobs."""
    pass


@jobs.command("list")
@click.option("--name", help="Filter jobs by name (case-insensitive).")
@click.option("--status", help="Filter jobs by status (case-insensitive).")
@click.option("--sort-by", type=click.Choice(["name", "lastResult"], case_sensitive=False), help="Sort jobs by a specific field.")
@click.option("--output", type=click.Choice(["table", "json", "csv"], case_sensitive=False), default="table", help="Output format.")
def list_jobs(name, status, sort_by, output):
    """List backup jobs."""
    client = VeeamApiClient()
    response = client.get_backup_jobs()
    jobs = response.get("data", [])

    if name:
        jobs = [job for job in jobs if name.lower() in job["name"].lower()]
    if status:
        jobs = [job for job in jobs if status.lower() == job["lastResult"].lower()]

    if sort_by:
        jobs = sorted(jobs, key=lambda job: job[sort_by].lower())

    if output == "json":
        print(json.dumps(jobs, indent=2))
    elif output == "csv":
        if not jobs:
            return
        writer = csv.DictWriter(sys.stdout, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)
    else:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Last Result")

        for job in jobs:
            table.add_row(job["id"], job["name"], job["type"], job["lastResult"])

        console.print(table)

@jobs.command("get")
@click.argument("job_id")
def get_job(job_id):
    """Get sessions for a specific job."""
    client = VeeamApiClient()
    response = client.get_job_sessions(job_id)
    sessions = response.get("data", [])

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Status")
    table.add_column("Result")

    for session in sessions:
        table.add_row(
            session["startTime"],
            session["endTime"],
            session["status"],
            session["result"],
        )
    console.print(table)

@jobs.command("restore-points")
@click.argument("job_id")
def restore_points(job_id):
    """List restore points for a specific job."""
    client = VeeamApiClient()
    response = client.get_job_restore_points(job_id)
    restore_points = response.get("data", [])

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Creation Time")
    table.add_column("Type")
    table.add_column("Backup File")

    for rp in restore_points:
        table.add_row(rp["creationTime"], rp["type"], rp.get("backupFile", "N/A"))

    console.print(table)

@cli.group()
def repos():
    """Manage repositories."""
    pass

@repos.command("list")
@click.option("--sort-by", type=click.Choice(["name", "capacity", "freeSpace"], case_sensitive=False), help="Sort repositories by a specific field.")
@click.option("--output", type=click.Choice(["table", "json", "csv"], case_sensitive=False), default="table", help="Output format.")
def list_repos(sort_by, output):
    """List repositories."""
    client = VeeamApiClient()
    response = client.get_repositories()
    repos = response.get("data", [])

    if sort_by:
        repos = sorted(repos, key=lambda repo: repo[sort_by])

    if output == "json":
        print(json.dumps(repos, indent=2))
    elif output == "csv":
        if not repos:
            return
        writer = csv.DictWriter(sys.stdout, fieldnames=repos[0].keys())
        writer.writeheader()
        writer.writerows(repos)
    else:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Capacity")
        table.add_column("Free Space")

        for repo in repos:
            capacity_gb = f"{repo['capacity'] / 1024**3:.2f} GB"
            free_space_gb = f"{repo['freeSpace'] / 1024**3:.2f} GB"
            table.add_row(repo["name"], capacity_gb, free_space_gb)

        console.print(table)

@cli.group()
def tapes():
    """Manage tape libraries and drives."""
    pass

@tapes.command("list")
def list_tapes():
    """List tape libraries and drives."""
    client = VeeamApiClient()
    console = Console()

    # Libraries
    lib_response = client.get_tape_libraries()
    libraries = lib_response.get("data", [])
    lib_table = Table(show_header=True, header_style="bold magenta")
    lib_table.add_column("Name")
    lib_table.add_column("Type")
    lib_table.add_column("Status")
    console.print("Tape Libraries")
    for lib in libraries:
        lib_table.add_row(lib["name"], lib["type"], lib["status"])
    console.print(lib_table)

    # Drives
    drive_response = client.get_tape_drives()
    drives = drive_response.get("data", [])
    drive_table = Table(show_header=True, header_style="bold magenta")
    drive_table.add_column("Name")
    drive_table.add_column("Status")
    drive_table.add_column("Library")
    console.print("Tape Drives")
    for drive in drives:
        drive_table.add_row(drive["name"], drive["status"], drive["libraryName"])
    console.print(drive_table)


if __name__ == "__main__":
    cli()
