#!/usr/bin/python3
'''Tests for models/place.py.'''


import unittest
from models import place


class TestPlace(unittest.TestCase):
    '''Tests for Place model.'''

    def test_public_class_attribute_city_id(self):
        self.assertEqual(place.Place.city_id, '')

    def test_public_class_attribute_user_id(self):
        self.assertEqual(place.Place.user_id, '')

    def test_public_class_attribute_name(self):
        self.assertEqual(place.Place.name, '')

    def test_public_class_attribute_description(self):
        self.assertEqual(place.Place.description, '')

    def test_public_class_attribute_number_rooms(self):
        self.assertEqual(place.Place.number_rooms, 0)

    def test_public_class_attribute_number_bathrooms(self):
        self.assertEqual(place.Place.number_bathrooms, 0)

    def test_public_class_attribute_max_guest(self):
        self.assertEqual(place.Place.max_guest, 0)

    def test_public_class_attribute_price_by_night(self):
        self.assertEqual(place.Place.price_by_night, 0)

    def test_public_class_attribute_latitude(self):
        self.assertEqual(place.Place.latitude, 0.0)
        self.assertEqual(type(place.Place().latitude), float)

    def test_public_class_attribute_longitude(self):
        self.assertEqual(place.Place.longitude, 0.0)
        self.assertEqual(type(place.Place().longitude), float)

    def test_public_class_attribute_amenity_ids(self):
        self.assertEqual(place.Place.amenity_ids, [])
