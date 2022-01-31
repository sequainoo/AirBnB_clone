#!/usr/bin/python3
'''Test pep8 style for all modules.'''

import pep8
import unittest


class TestPep8(unittest.TestCase):
    '''Test pep8.'''
    def test_pep8(self):
        style = pep8.StyleGuide(quite=False)
        files = [
            'models/__init__.py',
            'models/base_model.py',
            'tests/__init__.py',
            'tests/test_pep8.py',
            'tests/test_models/__init__.py',
            'tests/test_models/test_base_model.py',
            'models/engine/__init__.py',
            'models/engine/file_storage.py',
            'console.py',
            'tests/test_models/test_state.py',
            'tests/test_models/test_city.py',
            'tests/test_models/test_amenity.py',
            'models/state.py',
            'models/user.py',
            'models/review.py',
            'models/place.py',
            'models/city.py',
            'models/amenity.py'
            ]
        errors = style.check_files(files).total_errors
        self.assertEqual(errors, 0, "fix pep8")
