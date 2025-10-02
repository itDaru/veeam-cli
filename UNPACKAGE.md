
# How to Unpackage and Run the Veeam B&R CLI

This document provides instructions on how to unpackage the project, install the dependencies, and run the CLI.

## 1. Unpackage the Archive

First, you need to unpackage the `veeam-cli.tar.xz` archive. You can do this with the following command:

```bash
tar -xf veeam-cli.tar.xz
```

This will create a directory with the project files.

## 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to install the dependencies. You can create and activate a virtual environment with the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install the Dependencies

Once the virtual environment is activated, you can install the project dependencies using pip:

```bash
pip install -r requirements.txt
```

If you want to run the tests or build the documentation, you also need to install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

## 4. Configure the .env File

Before you can use the CLI, you need to configure the connection to your Veeam Backup & Replication server. You can do this by creating a `.env` file in the root of the project.

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Then, edit the `.env` file with your Veeam server details:

```
VEEAM_HOST=veeam.example.com
VEEAM_PORT=9419
VEEAM_USER=your_user
VEEAM_PASSWORD=your_password
```

## 5. Run the CLI

Now you are ready to run the CLI. You can install the project in editable mode to make the `veeam-cli` command available in your shell:

```bash
pip install -e .
```

After the installation, you can use the `veeam-cli` command:

```bash
veeam-cli --help
veeam-cli jobs list
veeam-cli repos list
```
