
Usage
=====

The Veeam B&R CLI provides a set of commands to interact with the Veeam API.

List Backup Jobs
----------------

To list all backup jobs:

.. code-block:: bash

    veeam-cli jobs list

To filter jobs by name:

.. code-block:: bash

    veeam-cli jobs list --name <job_name>

To filter jobs by status:

.. code-block:: bash

    veeam-cli jobs list --status <status>

To sort jobs:

.. code-block:: bash

    veeam-cli jobs list --sort-by name

To change the output format:

.. code-block:: bash

    veeam-cli jobs list --output json

Get Job Sessions
----------------

To get the sessions for a specific job:

.. code-block:: bash

    veeam-cli jobs get <job_id>

List Restore Points
-------------------

To list the restore points for a specific job:

.. code-block:: bash

    veeam-cli jobs restore-points <job_id>

List Repositories
-----------------

To list all repositories:

.. code-block:: bash

    veeam-cli repos list

List Tape Resources
-------------------

To list all tape libraries and drives:

.. code-block:: bash

    veeam-cli tapes list
