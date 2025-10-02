# Veeam B&R CLI

![Veeam Logo](https://www.veeam.com/content/dam/veeam/global/logo/veeam_logo_white.svg)


A command-line interface (CLI) tool for interacting with the Veeam Backup & Replication API.

## Description

This tool allows you to manage and monitor your Veeam Backup & Replication environment from the command line. You can list backup jobs, repositories, and tape resources, as well as view detailed information about job sessions and restore points.

## Features

- **List backup jobs** with filtering and sorting options.
- **View detailed information** for each backup job session.
- **List restore points** for each backup job.
- **List repositories** and their free space.
- **List tape libraries and drives.**
- **Multiple output formats:** table, JSON, and CSV.

## Installation

1.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the CLI in editable mode:**

    ```bash
    pip install -e .
    ```

## Configuration

The CLI requires the following environment variables to be set:

-   `VEEAM_HOST`: The hostname or IP address of the Veeam Backup & Replication server.
-   `VEEAM_PORT`: The port of the Veeam Backup & Replication API (default: 9419).
-   `VEEAM_USER`: The username for authentication.
-   `VEEAM_PASSWORD`: The password for authentication.

You can set these variables in your shell or create a `.env` file in the project root.

```bash
cp .env.example .env
```

Then, edit the `.env` file with your Veeam server details.

## Usage

### Jobs

-   **List backup jobs:**

    ```bash
    veeam-cli jobs list
    ```

-   **Get job sessions:**

    ```bash
    veeam-cli jobs get <job_id>
    ```

-   **List restore points:**

    ```bash
    veeam-cli jobs restore-points <job_id>
    ```

### Repositories

-   **List repositories:**

    ```bash
    veeam-cli repos list
    ```

### Tapes

-   **List tape libraries and drives:**

    ```bash
    veeam-cli tapes list
    ```

## Dependencies

-   [click](https://click.palletsprojects.com/)
-   [requests](https://requests.readthedocs.io/)
-   [python-dotenv](https://github.com/theskumar/python-dotenv)
-   [rich](https://github.com/willmcgugan/rich)

## Roadmap

-   Implement email notifications for failed jobs.
-   Add a configuration file for API endpoint, credentials, and other settings.
-   Create an interactive mode for exploring the Veeam environment.
-   Add support for Veeam ONE reporting data.