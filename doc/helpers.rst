
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
Therefore, labels can be configured in a file *labels.cfg* within application folder.
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

.. note::

    The *labels* templatetag uses requested path to specify for which application a label is requested.
    Thus, path *stemp/index/* will try to load labels from application *stemp*.
    If no label is found or given (sub-) section is not found, *None* will be returned.
