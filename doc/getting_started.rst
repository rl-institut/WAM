Introduction
============

WAM-Server can be set up either manually (setting up database, environment and wam by hand) or via docker.
Both methods will be presented in the following.

.. contents::
   :depth: 3


Idea
----

WebAppMap-Server [WAM] provides a basic and expandable Django_ infrastructure to easily add applications.

.. _Django: https://www.djangoproject.com/

Installation via Docker
-----------------------

Prerequisites
^^^^^^^^^^^^^

* git is installed.
* Docker_ and Docker-Compose_ are installed.

.. _Docker: https://docs.docker.com/install/
.. _Docker-Compose: https://docs.docker.com/compose/install/


Setup
^^^^^

Following folder structure is recommended and used in the following:

.. code-block:: bash

  wam_docker
  +-- docker (Contains docker config and WAM code basis)
  |   +-- docker-compose.yml
  |   +-- WAM (WAM-Codebasis; WAM-apps are integrated here later)
  +-- config (Config for WAM and apps)
  |   +-- config.cfg

.. note::
  Changes to this structure have to be adopted in config file and docker config (docker-compose.yml)

Setup of folder structure and code basis:

.. code-block:: bash

  mkdir wam_docker
  cd wam_docker
  mkdir docker
  mkdir config
  cd docker
  git clone https://github.com/rl-institut/WAM.git
  cp WAM/docker-compose.yml .
  cp WAM/.config/config.cfg ../config/

Next, config files have to be adopted (`docker-compose.yml` und `config.cfg`).
Finally, following command builds image and starts new container:

.. code-block:: bash

  sudo docker-compose up -d --build

WAM-Server should now be available under 127.0.0.1:5000 !

.. _prerequisites:

Installation from Scratch
-------------------------

Prerequisites
^^^^^^^^^^^^^

- `PostgreSQL library <https://www.postgresql.org/download/>`_ should be installed.
- A PostgreSQL database should be created (see :ref:`postgresql`).
- `PostGIS` library should be installed (see :ref:`postgis`).
- if :ref:`celery_setup` shall be used, a :ref:`message_broker` must be used.

.. _postgresql:

PostgreSQL Setup
^^^^^^^^^^^^^^^^

This section describes the installtion of PostgreSQL on Linux and Windows.

Linux
*****

The following instructions are for Ubuntu and inspired from here_.

First, create a user name (here, *wam_admin* is used for the *USER* field of the config
file :ref:`configuration`)

.. code:: bash

    sudo -u postgres createuser --superuser wam_admin

Then enter in psql shell

.. code:: bash

    sudo -u postgres psql

There, change the password for the user *wam_admin*

.. code:: bash

     postgres=# \password wam_admin

Enter the same password you will use under the *PASSWORD* field in the config file
(:ref:`configuration`) and exit the shell with `\\q`

Then, create the database you will use under the *NAME* field in the config file
(:ref:`configuration`)

.. code:: bash

    sudo -u postgres createdb -O wam_admin wam_database

Whenever you want to use the database you should run

.. code:: bash

    sudo service postgresql start

This can be stopped using the command

.. code:: bash

    sudo service postgresql stop

.. _here: https://help.ubuntu.com/community/PostgreSQL

Windows
*******

1. Download and install latest `PostgreSQL for Windows <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>`_.

2. At the end of or after the install of PostgreSQL for Windows use `Stack Builder` (will be installed with PostgresSQL) to install `Spatial Extensions -> PostGIS bundle`

In the Windows command line (cmd.exe) or Powershell:

3. Set the path environment variable for PostgreSQL (to be able to use PostgreSQL via the command line), e.g.:

.. code::

    SETX PATH "%PATH%;C:\Program Files\PostgreSQL\11\bin"

4. Login to "psql" as user "postgres":

.. code::

    psql -U postgres

5. In psql create superuser "wam_admin":

.. code::

    CREATE ROLE wam_admin WITH LOGIN SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION;

6. Set a password for the superuser wam_admin:

.. code::

    \password wam_admin

7. Quit psql:

.. code::

    \q

8. Create database:

.. code::

    createdb -U wam_admin wam_database


How to start, stop and restart PostgreSQL on Windows:

1. Start:

.. code::

    pg_ctl -D "<drive letter>:\path\to\PostgreSQL\<version>\data" start

2. Stop:

.. code::

    pg_ctl -D "<drive letter>:\path\to\PostgreSQL\<version>\data" stop

3. Restart:

.. code::

    pg_ctl -D "<drive letter>:\path\to\PostgreSQL\<version>\data" restart

.. _postgis:

PostGIS Setup
^^^^^^^^^^^^^

This section describes the installtion of PostGIS on Linux and Windows.

Linux (Ubuntu)
**************


.. code:: bash

    sudo apt-get install binutils libproj-dev gdal-bin

.. code:: bash

    sudo apt-get install postgis postgresql-10-postgis-2.4


For other systems see https://postgis.net/.

Activate postgis extension (execute as SQL query) to make it work:

.. code:: bash

    CREATE EXTENSION postgis;

Windows
*******

If not already installed, use `Stack Builder` (will be installed with
PostgresSQL) to install `Spatial Extensions -> PostGIS bundle`


1. Login to psql as wam_admin in wam_database:

.. code::

    psql -U wam_admin wam_database


2. Create postgis extension:

.. code::

    CREATE EXTENSION postgis;

3. Quit psql:

.. code::

    \q

.. _message_broker:

Message Broker
^^^^^^^^^^^^^^

On our WAM-Server the message broker RabbitMQ_ is running in a docker container (see RabbitMQDocker_).
Developers allowed to use our service can connect to it by setting up a ssh-tunnel:

.. code:: bash

  ssh -fNL 5672:localhost:5672 wam_user@wam.rl-institut.de

Other users have to setup their own message broker

.. _RabbitMQ: https://www.rabbitmq.com/
.. _RAbbitMQDocker: https://hub.docker.com/_/rabbitmq/


.. _getting_started:

Getting Started
---------------

.. _setup_linux:

Setup on Linux:
^^^^^^^^^^^^^^^

Clone repository from GitHub via:

.. code:: bash

  git clone https://github.com/rl-institut/WAM.git

Setup conda environment with required packages via:

.. code:: bash

  conda env create -f environment.yml

Afterwards, applications can be "plugged-in" by simply cloning application into the root directory
and adding application name to environment variable *WAM_APPS* (see :ref:`environment`).
Requirements and configuration of an application can be found at :ref:`app_settings`

.. _environment_linux:

Linux: Environment Variables
****************************

WAM-Server needs at least the following environment variables:

- WAM_CONFIG_PATH: full path to the configuration file (see :ref:`configuration_file` for the file content)

- WAM_APPS: Apps which shall be loaded within *INSTALLED_APPS*. Additionally, individual app settings are loaded (see :ref:`app_settings`).

On Ubuntu, one can add them to the ``bashrc`` file, so that they are loaded automatically :

.. code:: bash

  nano ~/.bashrc

then add the following two lines

.. code:: bash

   export WAM_CONFIG_PATH=<path to your WAM repo>/.config/config.cfg
   export WAM_APPS=<name of wam app 1>,<name of wam app 2>

.. _configobj: https://configobj.readthedocs.io/en/latest/configobj.html

.. _setup_windows:

Setup on Windows:
^^^^^^^^^^^^^^^^^

Prerequisites:

- Git Bash (included in `Git for Windows <https://git-scm.com/>`_)
- Install the `small` version of Conda (Miniconda), the big version Anaconda is
  not needed (reverse install settings, include Anaconda to PATH but don't
  install as default): `Link <https://docs.conda.io/en/latest/miniconda.html>`_.


1. Open Git Bash and create a project folder

.. code:: bash

    mkdir project_folder_name
    cd project_folder_name

2. Clone repository from GitHub via:

.. code:: bash

  git clone https://github.com/rl-institut/WAM.git

3. Setup conda environment with required packages via:

.. code:: bash

  conda env create -f environment.yml

Afterwards, applications can be "plugged-in" by simply cloning application into the root directory
and adding application name to environment variable *WAM_APPS* (see :ref:`environment`).
Requirements and configuration of an application can be found at :ref:`app_settings`

4. Install package dependencies of your WAM app(s):

- Example app: `stemp_abw <https://github.com/rl-institut/WAM_APP_stemp_abw>`_

.. code:: bash

    conda install -c conda-forge gdal
    conda activate django
    conda install shapely
    pip install -r requirements.txt
    pip install -r stemp_abw/requirements.txt

.. _environment_windows:

Windows: Environment Variables
******************************

WAM-Server needs at least the following environment variables:

- WAM_CONFIG_PATH: full path to the configuration file (see :ref:`configuration_file` for the file content)

- WAM_APPS: Apps which shall be loaded within *INSTALLED_APPS*. Additionally, individual app settings are loaded (see :ref:`app_settings`).

Add them to your Windows user environment:

.. code::

   SETX WAM_CONFIG_PATH "<drive letter>:\<path to your WAM repo>\.config\config.cfg"
   SETX WAM_APPS "<name of wam app 1>,<name of wam app 2>"

.. _configuration_file:

Configuration file
^^^^^^^^^^^^^^^^^^

Configuration file located under the path given by *WAM_CONFIG_PATH* is loaded within *settings
.py*. The file is read in using python's configobj_ package.
The file should contain following sections:

- *[WAM]*: general config for the WAM-Server,
- *[DATABASE]*: with at least one default database connection, which will be used as django's database,
- *[CELERY]*: if celery is needed
- *[<APP_NAME>]*: Multiple sections containing config for each app

See minimal example config_file_:

.. literalinclude:: _static/config.cfg

.. _config_file: _static/config.cfg

Note: the indent level is important in the configuration file. Keywords are specified within ``[]``, they are analog to the
key in a python ``dict``. The nesting level of a keyword depends on the number of square brackets.


.. _server_deploy:

Deploying server without apps
-----------------------------

Even without adding apps into WAM, you can follow these steps to deploy the WAM server locally.

Make sure the postgresql_ service is running

.. code:: bash

    sudo service postgresql start

Then, run the following commands

.. code:: bash

    python manage.py makemigrations

.. code:: bash

    python manage.py migrate

.. code:: bash

    python manage.py createsuperuser

After the last command, follow the instructions inside the terminal and use the same values for
user and password as the *USER* and *PASSWORD* fields of the :ref:`configuration_file`.

Finally access to the WAM server with

.. code:: bash

    python manage.py runserver

.. _example_app_settings:

Example app
^^^^^^^^^^^

From the root level of the WAM repository, you can clone the app *WAM_APP_stemp_mv* with

.. code:: bash

    git clone https://github.com/rl-institut/WAM_APP_stemp_mv.git

For the time being you have to rename the app folder *stemp* and set your environment variable
*WAM_APPS* to *stemp*


.. _app_settings:

Deploying server with custom apps
---------------------------------

Requirements:

- *urls.py* which includes *app_name* equaling the app name and an index page, which is loaded as landing page by default

Additional setups:

- *settings.py* can setup additional parameters for projects *settings.py*.

If your app requires the use of additional packages, you should list them in the settings.py of your app (not the settings.py file form wam core) in the following way

.. code:: python

    INSTALLED_APP = ['package1', 'package2']

Then, wam core will manage the packages' installation and avoid duplicate installations between the different apps.


- *app_settings.py* contains application specific settings and is loaded at start of django server at the end of *settings.py*. This file may include additional database connections, loading of config files needed for the application, etc.


.. warning:: Avoid using config variables for packages in your app as it may override or get overridden by package config of other app!


- *labels.cfg* (uses configobj_) supports easy adding of labels to templates via templatetags (see :ref:`label_tags`)


To install the required packages for each app run

.. code:: bash

    python install_requirements.py

from the root level of the WAM repository. Then follow the procedure described under :ref:`server_deploy`


.. _use_celery:

Celery
------

Celery_ is included in WAM. In order to use celery in an app, follow the :ref:`setup`.

.. _Celery: http://docs.celeryproject.org/en/latest/

.. _celery_setup:

Setup
^^^^^

- :ref:`message_broker` has to be running.
- Celery must be configured to use the message broker (see :ref:`configuration`).
- Run celery from WAM root directory via command (environment_ variables have to be set!):

.. code:: bash

  celery -A wam worker -Q wam_queue -l info

- After running above command, celery searches for *tasks.py* in every app and "activates" all tasks in it.
- WAM-apps are now able to run celery :ref:`celery_tasks`!

.. _celery_tasks:

Tasks
^^^^^

Celery tasks are easy...

You simply have to create a *task.py* in your app and put *from wam.celery import app* at beginning of the module.
Then, "normal" python functions can be turned into celery tasks using decorator *@app.task*.
See minimal example:

.. literalinclude:: _static/tasks.py

Afterwards, the task can be imported, run and controlled from elsewhere:

.. literalinclude:: _static/run_tasks.py

.. note::
  Input parameters and output results of celery tasks must be pickleable or jsonable.
  In order to use Django models within the celery task you should exchange primary keys
  (see also https://oddbird.net/2017/03/20/serializing-things/).

See http://docs.celeryproject.org/en/latest/userguide/tasks.html for more information on tasks.

