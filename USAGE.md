
# Veeam B&R CLI Usage

This document provides instructions on how to install, configure, and use the Veeam B&R CLI tool.

## Installation

To install the Veeam B&R CLI, you can use pip:

```bash
pip install veeam-cli
```

## Configuration

The CLI requires the following environment variables to be set:

- `VEEAM_HOST`: The hostname or IP address of the Veeam Backup & Replication server.
- `VEEAM_PORT`: The port of the Veeam Backup & Replication API (default: 9419).
- `VEEAM_USER`: The username for authentication.
- `VEEAM_PASSWORD`: The password for authentication.

You can set these variables in your shell, or create a `.env` file in the directory where you run the CLI.

**.env file example:**

```
VEEAM_HOST=veeam.example.com
VEEAM_PORT=9419
VEEAM_USER=your_user
VEEAM_PASSWORD=your_password
```

### Authentication and Tokens

The Veeam B&R CLI handles authentication and token management automatically. When you run a command, the tool will first authenticate with the Veeam API using the credentials provided in the environment variables or the `.env` file. It will then obtain an access token and a refresh token.

The access token is used to authenticate subsequent requests to the API. The tool stores these tokens in memory and will automatically refresh the access token when it expires using the refresh token. You do not need to manually extract or manage any tokens.

## Usage

The Veeam B&R CLI provides a set of commands to interact with the Veeam API.

### List Backup Jobs

To list all backup jobs:

```bash
veeam-cli jobs list
```

To filter jobs by name:

```bash
veeam-cli jobs list --name <job_name>
```

To filter jobs by status:

```bash
veeam-cli jobs list --status <status>
```

To sort jobs:

```bash
veeam-cli jobs list --sort-by name
```

To change the output format:

```bash
veeam-cli jobs list --output json
```

### Get Job Sessions

To get the sessions for a specific job:

```bash
veeam-cli jobs get <job_id>
```

### List Restore Points

To list the restore points for a specific job:

```bash
veeam-cli jobs restore-points <job_id>
```

### List Repositories

To list all repositories:

```bash
veeam-cli repos list
```

### List Tape Resources

To list all tape libraries and drives:

```bash
veeam-cli tapes list
```
