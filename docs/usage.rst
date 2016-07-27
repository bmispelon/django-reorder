========
Usage
========


.. module:: django_reorder.reorder

To use Django Reorder in a project::

    from django_reorder.reorder import reorder


Consider the following model::

    SIZES = [
        ('XXS', 'XX-Small'),
        ('XS', 'X-Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('XXL', 'XX-Large'),
    ]


    class Tshirt(models.Model):
        name = models.CharField(max_length=100)
        size = models.CharField(max_length=5, choices=SIZES)

        def __str__(self):
            return self.name


If you try to do something like ``Tshirt.objects.order_by('size')``, then you
get alphabetical sorting on the size (L, M, S, XL, XS, XXL, XXS) which is
probably not what you want.

With django-reorder, you can do::

    Tshirt.objects.order_by(reorder(size=['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']))

And your tshirts will be sorted by their size.


Reference
=========

.. function:: reorder(<fieldname>=<new order>, _default=AFTER, _reverse=False)

    This function generates a query expression (suitable for passing directly
    in ``order_by`` or ``annotate``) that will sort the queryset by the given
    ``<fieldname>`` so that rows appear in the order given by ``<new_order>``.

    It takes two optional parameters (their names are prefixed by an
    underscore to prevent clashing with potential field names):
    
    * ``_default`` controls whether values that don't appear in ``<new order>``
      are sorted before or after (the default) those that do.
      Use the ``BEFORE`` and ``AFTER`` constants that can be imported from the module.

    * ``_reverse`` lets you reverse the sorting.
