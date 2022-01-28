#!/usr/bin/python3
'''This module has User model implementation.'''

import models
from models import base_model
class User(base_model.BaseModel):
    '''User Model.'''

    email = ''
    password = ''
    first_name = ''
    last_name = ''