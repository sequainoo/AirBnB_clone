#!/usr/bin/python3
'''Tests for models/amenity.py.'''


import unittest
from models import amenity


class TestAmenity(unittest.TestCase):
    '''Tests for Amenity model.'''

    def test_public_class_attribute_name(self):
        '''Tests name has default value of ''.'''
        self.assertEqual(amenity.Amenity.name, '')
        self.assertEqual(amenity.Amenity().name, '')
