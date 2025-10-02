
Installation
============

To install the Veeam B&R CLI, you can use pip:

.. code-block:: bash

    pip install veeam-cli

Configuration
-------------

The CLI requires the following environment variables to be set:

- `VEEAM_HOST`: The hostname or IP address of the Veeam Backup & Replication server.
- `VEEAM_PORT`: The port of the Veeam Backup & Replication API (default: 9419).
- `VEEAM_USER`: The username for authentication.
- `VEEAM_PASSWORD`: The password for authentication.

You can set these variables in your shell, or create a `.env` file in the directory where you run the CLI.

.env file example:

.. code-block::

    VEEAM_HOST=veeam.example.com
    VEEAM_PORT=9419
    VEEAM_USER=your_user
    VEEAM_PASSWORD=your_password
