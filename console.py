#!/usr/bin/env python3
'''AirBnB Console that interacts with data objects of the application.'''


import cmd
import models
from models import base_model, user, state, review, place, city, amenity


CLASSNAMES = {
    'BaseModel': base_model.BaseModel,
    'User': user.User,
    'State': state.State,
    'Review': review.Review,
    'Place': place.Place,
    'City': city.City,
    'Amenity': amenity.Amenity
}
storage = models.storage


class HBNBCommand(cmd.Cmd):
    '''The Console'''

    prompt = '(hbnb) '

    def do_quit(self, arg):
        '''Quit command to exit the console.
        '''
        return True

    def do_EOF(self, arg):
        '''Quit command to exit the console.
        '''
        return True

    def emptyline(line):
        '''Empty lines executes nothing.'''
        pass

    def do_create(self, class_name):
        '''Creates a new instance of BaseModel, saves it and prints the id.'''
        if not class_name:
            print('** class name missing **')
        elif class_name not in CLASSNAMES:
            print('** class doesn\'t exist ** ')
        else:
            instance = CLASSNAMES[class_name]()
            instance.save()
            print(instance.id)

    def do_show(self, args):
        '''Prints the str representation of an instance.

        Based on class name and id.
        '''
        args = self.parse_args_2(args)
        if args is None:
            return
        class_name, _id = args
        search_key = self.key_from_storage(class_name, _id)
        print(storage.all()[search_key])

    def do_destroy(self, args):
        '''Deletes an instance.

        Based on the class name and id.
        Saves changes to file.
        '''
        args = self.parse_args_2(args)
        if args is None:
            return
        class_name, _id = args
        search_key = self.key_from_storage(class_name, _id)
        storage.all().pop(search_key)
        storage.save()

    def do_all(self, class_name):
        '''Prints str representation of all instances.

        Based on or not on class name.
        '''
        _list = []
        if not class_name:
            for key, instance in storage.all().items():
                _list.append(str(instance))
            print(_list)
            return
        if class_name in CLASSNAMES:
            for key, instance in storage.all().items():
                if key.startswith(class_name):
                    _list.append(str(instance))
            print(_list)
        else:
            print('** class doesn\'t exist **')

    def do_update(self, args):
        '''Updates an instance based on class name and id.'''
        args = self.parse_args_for_update(args)
        if args is None:
            return
        class_name, _id, attr_name, attr_value = args
        search_key = self.key_from_storage(class_name, _id)
        obj = self.find_obj(search_key)
        if obj is None:
            return
        existing_attr = getattr(obj, attr_name, None)
        if existing_attr is None:
            setattr(obj, attr_name, attr_value)
        else:
            attr_value = type(existing_attr)(attr_value)
            setattr(obj, attr_name, attr_value)
        storage.save()

    @staticmethod
    def find_obj(key):
        return storage.all().get(key, None)

    @staticmethod
    def parse_args_for_update(args):
        '''Parse args line <class name> <id> <attr name> "<attr value>".'''
        line = args
        if not args:
            print('** class name missing **')
            return
        args = args.split()
        if len(args) < 2:
            print('** instance id missing **')
            return
        if len(args) < 3:
            print('** attribute name missing **')
            return
        if len(args) < 4:
            print('** value missing **')
            return
        class_name, _id, attr_name = args[:3]
        start = line.index('"') + 1
        end = line.index('"', start)
        attr_value = line[start:end]

        if class_name not in CLASSNAMES:
            print('** class doesn\'t exist **')
            return
        if HBNBCommand.key_from_storage(class_name, _id) not in storage.all():
            print('** no instance found **')
            return
        return class_name, _id, attr_name, attr_value

    @staticmethod
    def parse_args_2(args):
        '''Parses the command arguments of 2.

        Returns:
            tuple: Tuple of 2 the class name and id, if valid arguments
            None: if valid arguments
        '''
        if not args:
            print('** class name missing **')
            return
        args = args.split()
        if len(args) < 2:
            print('** instance id missing **')
            return
        else:
            class_name, _id = args

        if class_name not in CLASSNAMES:
            print('** class doesn\'t exist ** ')
            return
        search_key = HBNBCommand.key_from_storage(class_name, _id)
        if search_key not in storage.all():
            print('** no instance found **')
            return
        return class_name, _id

    @staticmethod
    def key_from_storage(class_name, _id):
        '''Returns the Classname.id format key from the storage.'''
        return '{}.{}'.format(class_name, _id)


def main():
    '''entry point into the interpreter and the logic.'''
    console = HBNBCommand()
    console.cmdloop()


if __name__ == '__main__':
    main()
