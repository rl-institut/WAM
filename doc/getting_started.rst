
Getting started
===============

.. toctree::
   :maxdepth: 1

Idea
----

WebAppMap-Server [WAM] provides a basic and expandable Django_ infrastructure to easily add applications.

.. _Django: https://www.djangoproject.com/

Prerequisites
-----
Install:
- `postgresql` library should be installed (https://www.postgresql.org/download/ ).
- A postgresql database should be created (see :ref:`postgresql`).
- `postgis` library should be installed (see :ref:`postgis`).


Setup
-----

Clone repository from gogs via:

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
The file should contain a *[DATABASE]* section with at least one default database connection, which will be used as django's database:

.. code:: text

   [DATABASES]
       [[DEFAULT]]
           ENGINE = postgresql
           HOST = localhost
           PORT = 5432
           NAME = wam_database
           USER = wam_admin
           PASSWORD = wam_password

.. _environment:

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

WAM-Server needs at least the following environment variables:

- CONFIG_PATH: Path to configuration file (mainly includes database configurations, see :ref:`configuration`)
- DJANGO_SECRET_KEY: Set a secret key for *settings.py* (SECURITY WARNING: keep the secret key used in production secret!)
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

.. _postgresql:
postgresql setup
----------------
The following instructions are for Ubuntu and inpired from https://help.ubuntu.com/community/PostgreSQL
First create a user name (here *wam_admin* is used for the *USER* field of the config file
:ref:`configuration`)
.. code::bash
    sudo -u postgres createuser --superuser wam_admin

Then enter in psql shell

.. code::bash

    sudo -u postgres psql

There, change the password for the user *wam_admin*

.. code::bash

     postgres=# \password wam_admin

Enter the same password you will use under the *PASSWORD* field in the config file
(:ref:`configuration`) and exit the shell with `\q`

Create the database you will use under the *NAME* field in the config file
(:ref:`configuration`)

.. code::bash

    sudo -u postgres createdb -O wam_admin wam_database

Whenever you want to use the database you should run

.. code::bash

    sudo service postgresql start

This can be stopped using the command

.. code::bash

    sudo service postgresql stop

.. _postgis:
Postgis setup
-------
For Ubuntu:
.. code::bash

    sudo apt-get install binutils libproj-dev gdal-bin

.. code::bash

    sudo apt-get install postgis postgresql-10-postgis-2.4


For other systems see https://postgis.net/.