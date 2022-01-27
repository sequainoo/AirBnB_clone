#!/usr/bin/python3
'''
File storage.
Provides FileStorage class to store and retrive instances/objects
'''


class FileStorage():
    '''File storage class.

    Serializes instances to JSON file.
    Deserializes JSON file to instances.

    '''
    #: path to the JSON file ex: file.json
    __file_path = 'data.json'

    #: Stores all objects by <class name>.id ex: BaseModel.12121212
    __objects = {}

    def all(self):
        '''Returns the dictionary __objects.'''
        return self.__class__.__objects
    
    def new(self, obj):
        '''Sets in __objects the obj with key <obj class name>.id.'''
        pass
    
    def save(self):
        '''Serializes __objects to the JSON file (path: __file_path)'''
        pass
    
    def reload(self):
        '''
        Deserializes the JSON file to __objects only if the file exists.
        Otherwise, do nothing.
        '''
        pass
