#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-reorder
------------

Tests for `django-reorder` models module.
"""
from operator import attrgetter

from django.test import TestCase

from django_reorder.reorder import reorder, BEFORE, AFTER

from .models import Tshirt


class TestDjango_reorder(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tshirt.objects.create(name='DjangoCon US 2016', size='M')
        Tshirt.objects.create(name='DjangoCon Europe 2012', size='L')
        Tshirt.objects.create(name='PyCon US 2014', size='XXS')
        Tshirt.objects.create(name='Django Under the Hood 2015', size='XXL')

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
                'DjangoCon US 2016',
                'DjangoCon Europe 2012',
                'Django Under the Hood 2015',
            ],
            transform=attrgetter('name')
        )

    def test_reorder_after(self):
        sizes = list('XS S M L XL XXL'.split())  # leaving out XXL
        queryset = Tshirt.objects.order_by(reorder(size=sizes, _default=AFTER))
        self.assertQuerysetEqual(
            queryset,
            [
                'DjangoCon US 2016',
                'DjangoCon Europe 2012',
                'Django Under the Hood 2015',
                'PyCon US 2014',
            ],
            transform=attrgetter('name')
        )

    def test_reorder_before(self):
        sizes = list('XXS XS S M L XL'.split())  # leaving out XXS
        queryset = Tshirt.objects.order_by(reorder(size=sizes, _default=BEFORE))
        self.assertQuerysetEqual(
            queryset,
            [
                'Django Under the Hood 2015',
                'PyCon US 2014',
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
                'Django Under the Hood 2015',
                'DjangoCon Europe 2012',
                'DjangoCon US 2016',
                'PyCon US 2014',
            ],
            transform=attrgetter('name')
        )
