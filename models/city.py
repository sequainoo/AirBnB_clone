#!/usr/bin/python3
'''Module implements the City model.'''


from models import base_model


class City(base_model.BaseModel):
    '''City models a country's city.

    Attributes:
        name (str): Name of the state.

    '''

    state_id = ''
    name = ''
