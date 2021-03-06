#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-reorder
------------

Tests for `django-reorder` models module.
"""
from operator import attrgetter

from django.test import TestCase

from django_reorder.reorder import null_first, null_last, reorder, BEFORE, AFTER

from .models import Sleeve, Tshirt


class TestDjango_reorder(TestCase):

    @classmethod
    def setUpTestData(cls):
        pycon_us_2014 = Tshirt.objects.create(name='PyCon US 2014', size='XXS')
        pycon_us_2015 = Tshirt.objects.create(name='PyCon US 2015', size='XXS')
        djcon_us_2016 = Tshirt.objects.create(name='DjangoCon US 2016', size='M')
        djcon_eu_2012 = Tshirt.objects.create(name='DjangoCon Europe 2012', size='L')
        djcon_eu_2017 = Tshirt.objects.create(name='DjangoCon Europe 2017', size='XXL')

        Sleeve.objects.create(tshirt=pycon_us_2014, length=30)
        Sleeve.objects.create(tshirt=pycon_us_2014, length=35)
        Sleeve.objects.create(tshirt=djcon_us_2016, length=10)
        Sleeve.objects.create(tshirt=djcon_us_2016, length=30)
        Sleeve.objects.create(tshirt=djcon_eu_2012, length=20)
        Sleeve.objects.create(tshirt=djcon_eu_2017, length=40)

    def test_function_signature(self):
        with self.assertRaises(TypeError):
            reorder()

    def test_simple_reorder(self):
        sizes = list('XXS XS S M L XL XXL'.split())
        queryset = Tshirt.objects.order_by(reorder(size=sizes))
        self.assertQuerysetEqual(
            queryset,
            [
                'PyCon US 2014',
                'PyCon US 2015',
                'DjangoCon US 2016',
                'DjangoCon Europe 2012',
                'DjangoCon Europe 2017',
            ],
            transform=attrgetter('name')
        )

    def test_reorder_after(self):
        sizes = list('XS S M L XL XXL'.split())  # leaving out XXS
        queryset = Tshirt.objects.order_by(reorder(size=sizes, _default=AFTER))
        self.assertQuerysetEqual(
            queryset,
            [
                'DjangoCon US 2016',
                'DjangoCon Europe 2012',
                'DjangoCon Europe 2017',
                'PyCon US 2014',
                'PyCon US 2015',
            ],
            transform=attrgetter('name')
        )

    def test_reorder_before(self):
        sizes = list('XXS XS S M L XL'.split())  # leaving out XXL
        queryset = Tshirt.objects.order_by(reorder(size=sizes, _default=BEFORE))
        self.assertQuerysetEqual(
            queryset,
            [
                'DjangoCon Europe 2017',
                'PyCon US 2014',
                'PyCon US 2015',
                'DjangoCon US 2016',
                'DjangoCon Europe 2012',
            ],
            transform=attrgetter('name')
        )

    def test_reverse(self):
        sizes = list('XXS XS S M L XL XXL'.split())
        queryset = Tshirt.objects.order_by(reorder(size=sizes, _reverse=True))
        self.assertQuerysetEqual(
            queryset,
            [
                'DjangoCon Europe 2017',
                'DjangoCon Europe 2012',
                'DjangoCon US 2016',
                'PyCon US 2014',
                'PyCon US 2015',
            ],
            transform=attrgetter('name')
        )

    def test_join_foreignkey(self):
        sizes = list('XXS XS S M L XL XXL'.split())
        queryset = Sleeve.objects.order_by(reorder(tshirt__size=sizes))
        self.assertQuerysetEqual(queryset, [30, 35, 10, 30, 20, 40], transform=attrgetter('length'))

    def test_join_foreignkey_plus_order_by(self):
        djcon_us_2016 = Tshirt.objects.get(name='DjangoCon US 2016')
        queryset = Sleeve.objects.order_by(reorder(tshirt=[djcon_us_2016]), 'length')
        self.assertQuerysetEqual(queryset, [10, 30, 20, 30, 35, 40], transform=attrgetter('length'))

    def test_null_first(self):
        Sleeve.objects.create(length=5)
        Sleeve.objects.create(length=50)
        queryset = Sleeve.objects.order_by(null_first('tshirt'), 'length')
        self.assertQuerysetEqual(queryset, [5, 50, 10, 20, 30, 40], transform=attrgetter('length'))

        queryset = Sleeve.objects.order_by(null_first('tshirt'), '-length')
        self.assertQuerysetEqual(queryset, [50, 5, 40, 30, 20, 10], transform=attrgetter('length'))

    def test_null_last(self):
        Sleeve.objects.create(length=5)
        Sleeve.objects.create(length=50)
        queryset = Sleeve.objects.order_by(null_last('tshirt'), 'length')
        self.assertQuerysetEqual(queryset, [10, 20, 30, 40, 5, 50], transform=attrgetter('length'))

        queryset = Sleeve.objects.order_by(null_last('tshirt'), '-length')
        self.assertQuerysetEqual(queryset, [40, 30, 20, 10, 50, 5], transform=attrgetter('length'))
