#!/usr/bin/python3
'''
File storage.
Provides FileStorage class to store and retrive instances/objects
'''

import json

class FileStorage():
    '''File storage class.

    Serializes instances to JSON file.
    Deserializes JSON file to instances.

    '''
    #: path to the JSON file ex: file.json
    __file_path = './data/file_db.json'

    #: Stores all objects by <class name>.id ex: BaseModel.12121212
    __objects = {}

    def all(self):
        '''Returns the dictionary __objects.'''
        return FileStorage.__objects
    
    def new(self, obj):
        '''Sets in __objects the obj with key <obj class name>.id.'''
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj
    
    def save(self):
        '''Serializes __objects to the JSON file (path: __file_path)'''
        file_path = FileStorage.__file_path
        data = {}
        for key,obj in FileStorage.__objects.items():
            data[key] = obj.to_dict()
        
        with open(file_path, mode='w', encoding='utf-8') as file_obj:
            json.dump(data, file_obj)
    
    def reload(self):
        '''
        Deserializes the JSON file to __objects only if the file exists.
        Otherwise, do nothing.
        '''
        pass
