
API Changes
===========

List of API-Changes which have to be regarded when using WAM-Django-Backend.

7667dc9 (29.11.2018)
--------------------

Renamed utils.utils to utils.shortcuts

8ad8e54 (26.11.2018)
--------------------

Now, entire engine name has to be set in config-file.
Example for case of django backend:

.. code:: text

  # In config.cfg:

   [DATABASES]
       [[DEFAULT]]
           ENGINE = django.db.backends.postgresql  # instead of postgresql
           HOST = localhost
           PORT = 5432
           NAME = wam_database
           USER = wam_admin
           PASSWORD = wam_password

551866e (19.11.2018)
--------------------

In order to customize/edit admin site per app, the default admin site from `django.contrib.admin.site` is exchanged with `wam.admin.wam_admin_site`.
This new `AdminSite` class is used as default admin site for WAM-backend. Thus, **your models will not appear in admin site**, until you changed your code to use `wam_admin_site` instead.
Fortunately, this is very easy...

Instead of this "normal" looking admin.py file in app-folder:

.. code:: python

  from django.contrib import admin
  from my_app import models

  admin.site.register(models.MyModel)

Simply import wam_admin_site and register your model there:

.. code:: python

  from wam.admin import wam_admin_site
  from my_app import models

  wam_admin_site.register(models.MyModel)

With this little change, everything works as expected.
But now, you are able to extend WAM-admin site!
See :ref:`custom_admin_site` for more information.

Links:

:General: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#module-django.contrib.admin
:Custom: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#customizing-the-adminsite-class
:Admin-URLS: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls

