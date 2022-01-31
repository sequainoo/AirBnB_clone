#!/usr/bin/python3
'''Tests for models/city.py.'''


import unittest
from models import city


class TestCity(unittest.TestCase):
    '''Tests for the City model.'''

    def test_public_class_attribute_state_id(self):
        '''Tests state_id is '' by default.'''
        self.assertEqual(city.City.state_id, '')
        self.assertEqual(city.City().state_id, '')

    def test_public_class_attribute_name(self):
        '''Tests name is '' by default.'''
        self.assertEqual(city.City.name, '')
        self.assertEqual(city.City().name, '')
