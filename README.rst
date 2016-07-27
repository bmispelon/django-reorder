=============================
Django Reorder
=============================

.. image:: https://badge.fury.io/py/django-reorder.png
    :target: https://badge.fury.io/py/django-reorder

A project that helps sorting querysets in a specific order

Documentation
-------------

The full documentation is at https://django-reorder.readthedocs.org.

Quickstart
----------

Install Django Reorder::

    pip install django-reorder

Then use it in a project::

    from django_reorder.reorder import reorder

    Tshirt.objects.order_by(reorder(size=['S', 'M', 'L']))


Some more detailed examples can be foind on the :doc:`usage` page.

Features
--------

* Can be used in ``order_by()`` and in ``annotate()`` calls.
* Works across relationships.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
