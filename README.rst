.. image:: https://travis-ci.org/cfpb/wagtail-inventory.svg?branch=master
  :alt: Build Status
  :target: https://travis-ci.org/cfpb/wagtail-inventory

wagtail-inventory
=================

Search Wagtail pages by block type.

Wagtail Inventory adds the ability to search pages in your Wagtail site by the StreamField block types they contain. It adds a new Settings menu to the Wagtail admin site that allows you to search for pages that do or do not contain certain blocks. It supports searching both by Wagtail built-in blocks (like ``CharBlock``) as well as any custom blocks you might define.

Setup
-----

Install the package using pip:

.. code-block:: bash

  $ pip install wagtail-inventory
 
Add ``wagtailinventory`` as an installed app in your Django settings:

.. code-block:: python

  # in settings.py
  INSTALLED_APPS = (
      ...
      'wagtailinventory',
      ...
  )

Run migrations to create required database tables:

.. code-block:: bash

  $ manage.py migrate wagtailinventory

Run a management command to initialize database tables with current pages:

.. code-block:: bash

  $ manage.py block_inventory

You should now be able to search your pages in the Wagtail admin site, under Settings > Block Inventory.

Compatibility
-------------

This code has been tested for compatibility with:

* Python 2.7, 3.5, 3.6
* Django 1.8 - 1.11, 2.0
* Wagtail 1.8 - 1.13, 2.0 - 2.1

Testing
-------

Run unit tests with ``tox`` to test against select supported package combinations.

Open source licensing info
--------------------------

#. `TERMS <https://github.com/cfpb/wagtail-inventory/blob/master/TERMS.md>`_
#. `LICENSE <https://github.com/cfpb/wagtail-inventory/blob/master/LICENSE>`_
#. `CFPB Source Code Policy <https://github.com/cfpb/source-code-policy>`_
