
Getting started
===============

.. toctree::
   :maxdepth: 1

Idea
----

WebAppMap-Server [WAM] provides a basic and expandable Django_ infrastructure to easily add applications.

.. _Django: https://www.djangoproject.com/

Setup
-----

Clone repository from gogs via:

.. code:: bash

  git clone https://wam.rl-institut.de:86/Hendrik/WAM.git

Setup conda environment with required packages via:

.. code:: bash

  conda env create -f env_requirements.yml

Afterwards, applications can be "plugged-in" by simply cloning application into wam folder
and activating app by adding application name to environment variable *WAM_APPS* (see :ref:`environment`).
Requirements and configuration of an application can be found at :ref:`app_settings`

.. _configuration:

Configuration
-------------

The WAM-Server can be configured as follows.

Configuration file
^^^^^^^^^^^^^^^^^^

Configuration file from path given by *CONFIG_PATH* is loaded within *settings.py*. The file is read in by pythons configobj_ package.
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
- DJANGO_SECRET_KEY: Set a secret key for *settings.py* (from *settings.py*: SECURITY WARNING: keep the secret key used in production secret!)
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
