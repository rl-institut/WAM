Edit documentation
==================

Idea
----

If a user want to improve the documentation, here is how to produce html files locally before
pushing the changes to the repository.

Getting Started
---------------

First, you have to install the sphinx package:

.. code:: bash

    pip install sphinx

Then, from the root of the WAM repository, run the following command to compile your documentation:

.. code:: bash

    make html

The html file will be available under doc/_build/html/index.html.