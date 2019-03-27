
Getting started
===============

.. contents::
   :depth: 2

Idea
----

WebAppMap-Server [WAM] provides a basic and expandable Django_ infrastructure to easily add applications.

.. _Django: https://www.djangoproject.com/

Prerequisites
-------------

- `postgresql library <https://www.postgresql.org/download/>`_ should be installed.
- A postgresql database should be created (see :ref:`postgresql`).
- `postgis` library should be installed (see :ref:`postgis`).
- if :ref:`celery_setup` shall be used, a :ref:`message_broker`  must be used.

.. _postgresql:

postgresql setup
^^^^^^^^^^^^^^^^

The following instructions are for Ubuntu and inpired from `here`__
First create a user name (here *wam_admin* is used for the *USER* field of the config file
:ref:`configuration`)

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

Create the database you will use under the *NAME* field in the config file
(:ref:`configuration`)

.. code:: bash

    sudo -u postgres createdb -O wam_admin wam_database

Whenever you want to use the database you should run

.. code:: bash

    sudo service postgresql start

This can be stopped using the command

.. code:: bash

    sudo service postgresql stop

__ https://help.ubuntu.com/community/PostgreSQL


.. _postgis:

Postgis setup
^^^^^^^^^^^^^

For Ubuntu:

.. code:: bash

    sudo apt-get install binutils libproj-dev gdal-bin

.. code:: bash

    sudo apt-get install postgis postgresql-10-postgis-2.4


For other systems see https://postgis.net/.


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

Setup
-----

Clone repository from github via:

.. code:: bash

  git clone https://github.com/rl-institut/WAM.git

Setup conda environment with required packages via:

.. code:: bash

  conda env create -f environment.yml

Afterwards, applications can be "plugged-in" by simply cloning application into the root directory
and adding application name to environment variable *WAM_APPS* (see :ref:`environment`).
Requirements and configuration of an application can be found at :ref:`app_settings`


.. _configuration:

Configuration
-------------

The WAM-Server can be configured as follows.

Configuration file
^^^^^^^^^^^^^^^^^^

Configuration file from path given by *CONFIG_PATH* is loaded within *settings.py*. The file is
read in using python's configobj_ package.
The file should contain following sections:

- *[WAM]*: general config for the WAM-Server,
- *[DATABASE]*: with at least one default database connection, which will be used as django's database,
- *[CELERY]*: if celery is needed
- *[<APP_NAME>]*: Multiple sections containing config for each app

See minimal example config_file_:

.. literalinclude:: _static/config.cfg

.. _config_file: _static/config.cfg

.. _environment:

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

WAM-Server needs at least the following environment variables:

- CONFIG_PATH: Path to configuration file (mainly includes database configurations, see :ref:`configuration`)
- WAM_APPS: Apps which shall be loaded within *INSTALLED_APPS*. Additionally, individual app settings are loaded (see :ref:`app_settings`).

.. _configobj: https://configobj.readthedocs.io/en/latest/configobj.html

.. _app_settings:

App Setup
---------

Requirements:

- *urls.py* which includes *app_name* equaling the app name and an index page, which is loaded as landing page by default

Additional setups:

- *settings.py* can setup additional parameters for projects *settings.py*
- *app_settings.py* contains application specific settings and is loaded at start of django server at the end of *settings.py*. This file may include additional database connections, loading of config files needed for the application, etc.
- *labels.cfg* (uses configobj_) supports easy adding of labels to templates via templatetags (see :ref:`label_tags`)


To install the required packages for each app run

.. code:: bash

    python install_requirements.py

from the root level of the WAM repository.


Make sure the postgresql_ service is running

.. code:: bash

    sudo service postgresql start

Then run the following commands

.. code:: bash

    python manage.py makemigrations

.. code:: bash

    python manage.py migrate

.. code:: bash

    python manage.py createsuperuser

upon the last command follow the instructions inside the terminal and use the same values for
user and password as the *USER* and *PASSWORD* fields of the config file
:ref:`configuration`.

Finally access to the WAM server by running

.. code:: bash

    python manage.py runserver


Example app:

From the root level of the WAM repository, you can clone the app *WAM_APP_stemp_mv* with

.. code:: bash

    git clone https://github.com/rl-institut/WAM_APP_stemp_mv.git

For the time being you have to rename the app folder *stemp* and set your environment variable
*WAM_APPS* to *stemp*

.. _celery_setup:

Celery
------

Celery_ is included in WAM. In order to use celery in an app, follow the :ref:`setup`.

.. _Celery: http://docs.celeryproject.org/en/latest/

.. _setup:

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

