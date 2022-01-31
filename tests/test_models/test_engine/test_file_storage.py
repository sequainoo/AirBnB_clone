'''Tests for file_storage module.'''


import unittest
import models
from models import base_model
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''Tests for the units of FileStorage.'''

    def test_new(self):
        '''Tests new method.

        Checks that new object is added to storage.
        '''
        new_obj = base_model.BaseModel()
        storage = FileStorage()
        storage.new(new_obj)
        for key, obj in storage.all().items():
            if new_obj is obj:
                self.assertTrue(True)
                return
        self.assertFalse(False)
