#!/usr/bin/python3
'''Tests for models/review.py.'''


import unittest
from models import review


class TestReview(unittest.TestCase):
    '''Tests for Review model.'''

    def test_public_class_attribute_place_id(self):
        '''Tests default value.'''
        self.assertEqual(review.Review.place_id, '')

    def test_public_class_attribute_user_id(self):
        '''Tests default value.'''
        self.assertEqual(review.Review.user_id, '')

    def test_public_class_attribute_text(self):
        '''Tests default value.'''
        self.assertEqual(review.Review.text, '')
