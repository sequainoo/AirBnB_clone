#!/usr/bin/python3
'''Module implements State model.'''


from models import base_model


class Place(base_model.BaseModel):
    '''Place represents, place in a city that one can rent.'''

    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
