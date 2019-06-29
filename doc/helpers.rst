
Helpers
=======

Little helper functions and classes for several use-cases.


Group Permissions
-----------------
A TemplateView-mixin is provided, which checks if user is logged in and if user is member of certain groups.
To check group permissions on a TemplateView, simply inherit from GroupCheckMixin as well and define groups to check.

Example:

.. code:: python

    from django.views.generic import TemplateView
    from utils.permissions import GroupCheckMixin

    class MyView(GroupCheckMixin, TemplateView):
        groups_to_check = ['group1', 'group2']
        template_name = 'my_template.html'


.. _label_tags:

Labels
------

A templatetag *label* is provided to easily load labels into templates.
To do so, labels can be configured in a file *labels.cfg* within application folder.
Section, subsection, etc. are supported (use *:* to separate sections) to organize labels within needed structure.

Example:

.. code:: html

    <!-- Loads label-templatetag -->
    {% load labels %}

    <!-- Tries to load label 'description' from section 'general' and subsection 'landing_page' from labels.cfg -->
    {% label 'general:landing_page:title' %}

with *labels.cfg* as:

.. code:: text

    [general]
        [[landing_page]]
            title = Das ist die Startseite!

Additionally, the label template tag supports two attributes:

- `safe` (boolean, default=False): Can be set to allow import of html-code
- `app` (str, default=None): Can be set explicitly to load labels from given app (Must be set, if template tag is requested from widget or form template)

.. note::

    The *labels* templatetag uses requested path to specify for which application a label is requested.
    Thus, path *stemp/index/* will try to load labels from application *stemp*.
    If template tag is used within widget or form template, app attribute has to be set.
    If no label is found or given (sub-) section is not found, *None* will be returned.


Feedback Form
-------------

A feedback form is available which can be used in all apps. The feedback is send via e-mail using an Exchange account.
Required environment variables for the Exchange account are WAM_EXCHANGE_ACCOUNT, WAM_EXCHANGE_EMAIL and WAM_EXCHANGE_PW.

To use the form, just add the view to your urls like

.. code:: python

  # my_app/urls.py

  from utils.views import FeedbackView

  admin_url_patterns = [
      path(<path to other view>),
      ...,
      path('feedback/', FeedbackView.as_view(app_name='<my app name>'), name='feedback')
  ]

Make sure you have the parameter ``email`` set in your *app.cfg*, example:

.. code:: text

  # my_app/app.cfg
  category = app
  name = ...
  icon = ...
  email = 'address_of_app_admin@domain.tld'


.. _custom_admin_site:

Customizing Admin Site
----------------------

With custom admin site, it is possible to add app-specific views to admin pages.
The WAM-backend is configured to search for list `admin_url_patterns` in `urls.py` for every app.
Those urls are internally added in `AdminSite.get_url()`_ and are afterwards available on admin site.

.. _`AdminSite.get_url()`: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls

An additional view for admin site can now integrated via:

.. code:: python

  # my_app/urls.py

  from my_app import views

  admin_url_patterns = [
      path(
          'my_url',
          views.MyView.as_view(),
      ),
  ]

Afterwards, this view would be accessible (**to all users!**, see example below for admin-only-access) under *.../admin/my_url*.

An additional example can be found in `Stemp Tool MV`_

.. _`Stemp Tool MV`: https://github.com/rl-institut/WAM_APP_stemp_mv/blob/master/urls.py

.. code:: python

  from wam.admin import wam_admin_site
  from stemp import views_admin

  admin_url_patterns = [
      path(
          'stemp/manage',
          wam_admin_site.admin_view(views_admin.ManageView.as_view()),
          name='manage'
      ),
  ]

Please notice the wrapping of custom view into `wam_admin_site.admin_view` function - this will guarantee admin-only access!