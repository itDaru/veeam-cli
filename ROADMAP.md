# Roadmap: Veeam B&R CLI Reporting Tool

This document outlines the planned features and development timeline for the Veeam Backup & Replication CLI reporting tool.

## Phase 1: Core Functionality

### Authentication

- [x] **Implement authentication with the Veeam Backup & Replication API.**
  - **Programmer's To-Do:**
    - Use the `requests` library to send a POST request to the `/api/oauth2/token` endpoint.
    - The request body should be `x-www-form-urlencoded` and contain `grant_type=password`, `username`, and `password`.
    - Store the returned `access_token` and `refresh_token` in memory.
    - Implement a mechanism to automatically refresh the `access_token` using the `refresh_token` when it expires. This involves sending a POST request to the same `/api/oauth2/token` endpoint with `grant_type=refresh_token` and the `refresh_token`.
    - Handle the case where the refresh token has also expired, requiring the user to re-authenticate.

- [x] **Securely store credentials and API host information.**
  - **Programmer's To-Do:**
    - Use the `python-dotenv` library to load credentials from a `.env` file during development (`VEEAM_USER`, `VEEAM_PASSWORD`, `VEEAM_HOST`).
    - For production, instruct users to set environment variables or use a configuration file.

### API Interaction

- [x] **Create a client to interact with the Veeam API.**
  - **Programmer's To-Do:**
    - Create a Python class `VeeamApiClient`.
    - The constructor will handle authentication and store the API host address and API version.
    - All API requests will be methods of this class and will include the API version in the URL (e.g., `/api/v1/...`).
    - Implement robust error handling for API requests, specifically handling `401 Unauthorized`, `404 Not Found`, and `5xx` server errors with user-friendly messages.

- [x] **Implement methods to fetch backup job information.**
  - **Programmer's To-Do:**
    - Create a method `get_backup_jobs()`.
    - This method will send a GET request to the `/api/v1/jobs` endpoint.
    - The method will handle pagination using the `offset` and `limit` query parameters.
    - The method will return a list of job objects.

- [x] **Implement methods to fetch repository information.**
  - **Programmer's To-Do:**
    - Create a method `get_repositories()`.
    - This method will send a GET request to the `/api/v1/backupRepositories` endpoint.
    - The method will return a list of repository objects.

### Basic Reporting

- [x] **Create a CLI command to display a list of backup jobs and their status.**
  - **Programmer's To-Do:**
    - Use the `click` library to create a command `veeam-cli jobs list`.
    - The command will call the `get_backup_jobs()` method from the `VeeamApiClient`.
    - It will then iterate through the returned jobs and print the `name`, `type`, and `lastResult` of each job in a formatted table using the `rich` library.
    - Provide clear help text for the command and its options.

- [x] **Create a CLI command to display a list of repositories and their free space.**
  - **Programmer's To-Do:**
    - Use `click` to create a command `veeam-cli repos list`.
    - This command will call `get_repositories()`.
    - It will then print the `name`, `capacity`, and `freeSpace` of each repository in a formatted table.
    - Provide clear help text for the command and its options.

## Phase 2: Advanced Reporting & CLI Features

### Advanced Reporting

- [x] **Fetch and display detailed information for each backup job session.**
  - **Programmer's To-Do:**
    - Create a `veeam-cli jobs get <job_id>` command.
    - This command will make a GET request to `/api/v1/jobs/<job_id>/sessions` to get the sessions for a specific job.
    - Display session details like `startTime`, `endTime`, `status`, and `result`.

- [x] **Fetch and display information about restore points for each job.**
  - **Programmer's To-Do:**
    - Create a `veeam-cli jobs restore-points <job_id>` command.
    - This command will make a GET request to `/api/v1/jobs/<job_id>/restorePoints`.
    - Display restore point details like `creationTime`, `type`, and `backupFile`.

- [x] **Add reporting for tape libraries and drives.**
  - **Programmer's To-Do:**
    - Create a `veeam-cli tapes list` command.
    - This command will make a GET request to `/api/v1/tape/libraries` and `/api/v1/tape/drives`.
    - Display tape library and drive information.

### CLI Enhancements

- [x] **Utilize a library like `click` for a more robust CLI experience.**
  - **Programmer's To-Do:**
    - The project will use `click` for all CLI commands, as established in Phase 1.
    - Group commands logically (e.g., `jobs`, `repos`, `tapes`) using `click.Group`.

- [x] **Add filtering options to reports (e.g., by job name, status).**
  - **Programmer's To-Do:**
    - Use `click` options (e.g., `--name`, `--status`) to filter the results from the API.
    - Implement filtering logic within the CLI command functions.

- [x] **Add sorting options to reports (e.g., by start time, duration).**
  - **Programmer's To-Do:**
    - Use `click` options (e.g., `--sort-by`) to sort the results.
    - Implement sorting logic using Python's `sorted()` function.

- [x] **Implement different output formats (e.g., JSON, CSV, formatted tables).**
  - **Programmer's To-Do:**
    - Add an `--output` option to all list commands.
    - Implement functions to format the output as JSON, CSV, or a `rich` table.

## Phase 3: Packaging & Distribution

### Packaging

- [x] **Package the application for easy installation.**
  - **Programmer's To-Do:**
    - Use a `pyproject.toml` file to define project metadata and dependencies.
    - Use a modern build backend like `flit` or `poetry` to build the package.

- [x] **Create a `pyproject.toml` to manage dependencies and project metadata.**
  - **Programmer's To-Do:**
    - The `pyproject.toml` will include:
      - `[project]`: `name`, `version`, `description`, `authors`
      - `[project.dependencies]`: 
        - `click`: For creating the CLI.
        - `requests`: For making HTTP requests to the Veeam API.
        - `python-dotenv`: For managing environment variables.
        - `rich`: For creating rich, formatted tables in the terminal.
      - `[project.scripts]`: Define a console script entry point for the CLI.

### Testing

- [x] **Write unit tests for the API client.**
  - **Programmer's To-Do:**
    - Use the `pytest` framework.
    - Use the `requests-mock` library to mock API responses from the Veeam API.
    - Test the `VeeamApiClient` methods for correct API calls and data parsing.

- [x] **Write integration tests for the CLI commands.**
  - **Programmer's To-Do:**
    - Use `pytest` and `click.testing.CliRunner`.
    - Test the CLI commands with mocked API data to ensure correct output and behavior.

### Documentation

- [x] **Create comprehensive user documentation.**
  - **Programmer's To-Do:**
    - Use `Sphinx` to generate documentation.
    - Create a `docs` directory with reStructuredText (`.rst`) files.
    - Document the installation process, configuration, and all CLI commands.

- [x] **Add examples for all CLI commands.**
  - **Programmer's To-Do:**
    - Include code blocks with example command usage and output in the documentation.

## Future Goals

- [ ] **Implement email notifications for failed jobs.**
  - **Programmer's To-Do:**
    - Add a command `veeam-cli jobs watch` that runs in the background.
    - This command will periodically check for failed jobs and send an email using Python's `smtplib`.

- [ ] **Add a configuration file for API endpoint, credentials, and other settings.**
  - **Programmer's To-Do:**
    - Use a library like `configparser` or `PyYAML` to manage a configuration file.
    - The application will look for a configuration file in a default location (e.g., `~/.config/veeam-cli/config.ini`).
    - The order of precedence for settings will be: command-line options > environment variables > configuration file.

- [ ] **Create an interactive mode for exploring the Veeam environment.**
  - **Programmer's To-Do:**
    - Use a library like `prompt_toolkit` to create an interactive shell.
    - The shell will provide commands and auto-completion for exploring the Veeam API.

- [ ] **Add support for Veeam ONE reporting data.**
  - **Programmer's To-Do:**
    - Investigate the Veeam ONE API (if available) or database structure.
    - Create a new set of commands to query and display Veeam ONE data.
