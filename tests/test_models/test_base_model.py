#!/usr/bin/python3
'''Unit tests for base_model module.'''

import unittest
from models.base_model import BaseModel
import uuid
from datetime import datetime
from contextlib import redirect_stdout
from io import StringIO
from pprint import pprint, pformat


class AssertFunc(unittest.TestCase):
    '''A helper class with assert methods.'''

    def assertIsUuid(self, str_obj):
        '''assert str_obj is a valid uuid hex string.'''
        if type(str_obj) is not str:
            raise TypeError('Must be a str')
        try:
            uuid.UUID(hex=str_obj)
        except ValueError:
            assert False, "id is not a valid uuid"
        else:
            assert True

    def assertDatetimeEquals(self, dt_obj1, dt_obj2):
        '''Assert that 2 datetime objects are equivalent.

        ignoring minor difference in seconds.
        '''
        abs_timedelta = abs(dt_obj1 - dt_obj2)
        diff_in_seconds = abs_timedelta.seconds
        assert diff_in_seconds < 2, "Time is not equivalent"

    def assertDatetimeNotEquals(self, dt_obj1, dt_obj2):
        '''Assert 2 datetimes are not equal.'''
        assert dt_obj1 != dt_obj2, "Times are equivalent"

    def assertDatetimeGreater(self, dt_obj1, dt_obj2):
        '''Assert time1 > time2.'''
        assert dt_obj1 > dt_obj2, "Time 1 is not greater than time 2"

    def assertDatetimeLess(self, dt_obj1, dt_obj2):
        '''Assert time1 < time2.'''
        assert dt_obj1 < dt_obj2, "Time 1 is not less than time 2"


class TestBaseModel(AssertFunc):
    '''Unit tests for BaseModel class.'''

    def test_id_attribute(self):
        '''Test string and uniqueness.
        '''
        inst = BaseModel()
        inst1 = BaseModel()
        self.assertIsNotNone(inst.id)
        self.assertTrue(isinstance(inst.id, str))  # assert id is str
        self.assertIsUuid(inst.id)
        self.assertNotEqual(inst.id, inst1.id)

    def test_created_at_attribute(self):
        '''Test type and time created.'''
        inst = BaseModel()
        time_created = datetime.now()
        self.assertTrue(isinstance(inst.created_at, datetime))
        self.assertDatetimeEquals(inst.created_at, time_created)

    def test_updated_at(self):
        '''Test type and time.'''
        inst = BaseModel()
        self.assertTrue(isinstance(inst.updated_at, datetime))
        # assert that when created updated_at is same as created_at
        self.assertDatetimeEquals(inst.updated_at, inst.created_at)

    def test_updated_at_after_save(self):
        '''Test updated_at after update with save().'''
        inst = BaseModel()
        time_created = datetime.now()
        inst.save()
        now = datetime.now()
        self.assertDatetimeEquals(inst.updated_at, now)
        self.assertDatetimeNotEquals(inst.updated_at, time_created)
        self.assertDatetimeGreater(inst.updated_at, time_created)

    # def test___str__(self):
    #     '''Test with expected format.

    #     format: [<class name>] (<self.id>) <self.__dict__>
    #     '''
    #     inst = BaseModel()
    #     cls_name = inst.__class__.__name__
    #     _id = inst.id
    #     _dict = pformat(self.__dict__)
    #     expected = "[{}] ({}) {}".format(cls_name, _id, _dict)
    #     with StringIO() as buffer, redirect_stdout(buffer):
    #         str(inst)
    #         string = buffer.getvalue()
    #         self.assertEqual(string, expected)

    def test_to_dict_returns_a_dict(self):
        inst = BaseModel()
        self.assertTrue(isinstance(inst.to_dict(), dict))

    def test_to_dict_returns_instance___dict__(self):
        '''
        Test dict returns instance __dict__
        with __class__ key.
        '''
        inst = BaseModel()
        expected = {**inst.__dict__}
        expected['__class__'] = inst.__class__.__name__
        expected['updated_at'] = inst.updated_at.isoformat()
        expected['created_at'] = inst.created_at.isoformat()
        self.assertDictEqual(inst.to_dict(), expected)

    def test_to_dict_has_updated_at_and_created_at_as_str(self):
        '''Test they are iso format.'''
        inst = BaseModel()
        updated_at = inst.to_dict()['updated_at']
        created_at = inst.to_dict()['created_at']
        self.assertTrue(isinstance(updated_at, str))
        self.assertTrue(isinstance(created_at, str))
        self.assertEqual(updated_at, inst.updated_at.isoformat())
        self.assertEqual(created_at, inst.created_at.isoformat())
