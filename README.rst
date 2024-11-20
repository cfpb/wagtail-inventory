.. image:: https://github.com/cfpb/wagtail-inventory/workflows/test/badge.svg
  :alt: Build Status
  :target: https://github.com/cfpb/wagtail-inventory/actions/workflows/test.yml

wagtail-inventory
=================

Search Wagtail pages by block type.

Wagtail Inventory adds the ability to search pages in your Wagtail site by the StreamField block types they contain. It adds a new report to the Wagtail admin site that allows you to search for pages that do or do not contain certain blocks. It supports searching both by Wagtail built-in blocks (like ``CharBlock``) as well as any custom blocks you might define.

Setup
-----

Install the package using pip:

.. code-block:: bash

  $ pip install wagtail-inventory

Add `wagtailinventory`` as an installed app in your Django settings:

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

Admin users should now be able to search pages in the Wagtail admin site, under Reports > Block Inventory.

Other user groups may be granted access to the report by giving them the "Can view" "Page block" permission in Wagtail Group settings.

Compatibility
-------------

This code has been tested for compatibility with:

* Python 3.8, 3.12
* Django 4.2 (LTS), 5.0, 5.1
* Wagtail 6.2, 6.3 (LTS)

It should be compatible with all intermediate versions, as well.
If you find that it is not, please `file an issue <https://github.com/cfpb/wagtail-inventory/issues/new>`_.

Testing
-------

Running project unit tests requires `tox <https://tox.wiki/en/latest/>`_:

.. code-block:: bash

  $ tox

To run the test app interactively, run:

.. code-block:: bash

  $ tox -e interactive

Now you can visit http://localhost:8000/admin/ in a browser and log in with ``admin`` / ``changeme``.

Open source licensing info
--------------------------

#. `TERMS <https://github.com/cfpb/wagtail-inventory/blob/main/TERMS.md>`_
#. `LICENSE <https://github.com/cfpb/wagtail-inventory/blob/main/LICENSE>`_
#. `CFPB Source Code Policy <https://github.com/cfpb/source-code-policy>`_
