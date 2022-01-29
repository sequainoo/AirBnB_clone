#!/usr/bin/python3
'''Module implements State model.'''


from models import base_model


class State(base_model.BaseModel):
    '''State represents a country's state.

    Attributes:
        name (str): Name of the state.

    '''

    name = ''
