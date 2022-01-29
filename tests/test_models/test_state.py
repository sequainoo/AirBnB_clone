#!/usr/bin/python3
'''Tests for models/state.py.'''


import unittest
from models import state


class TestState(unittest.TestCase):
    '''Tests for State model.'''

    def test_public_class_attribute_name(self):
        self.assertEqual(state.State.name, '')
        self.assertEqual(state.State().name, '')
