#!/usr/bin/python3
'''Module implements the Review model.'''


from models import base_model


class Review(base_model.BaseModel):
    '''Review models a review of a place.

    Attributes:
        place_id: Id of the place reviewing
        user_id: Id of user reviewing
        text (str): Review text.

    '''

    place_id = ''
    user_id = ''
    text = ''
