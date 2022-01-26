'''Module for the base model.'''

from datetime import datetime
import uuid
from pprint import pprint, pformat


class BaseModel(object):
    '''Base model.

    Attributes:
        id (str): A uuid (universally unique id)
        created_at (datetime): Date and time created
        updated_at (datetime): Date and time updated

    '''

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        '''Format: [<class name>] (<self.id>) <self.__dict__>.'''
        format_str = '[{}] ({}) {}'
        cls_name = self.__class__.__name__
        _id = self.id
        _dict = pformat(self.__dict__)
        format_str.format(cls_name, _id, _dict)
        return format_str

    def save(self):
        '''Currently Updates updated_at attribute.'''
        self.updated_at = datetime.now()

    def to_dict(self):
        '''Returns a dictionary with all in __dict__ plus key __class__.'''
        _dict = {**self.__dict__, '__class__': self.__class__.__name__}
        _dict['updated_at'] = self.updated_at.isoformat()
        _dict['created_at'] = self.created_at.isoformat()
        return _dict
