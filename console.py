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

    def default(self, line):
        '''Handles commands like <cls name>.all().'''
        cmd = line.strip()

        # if cmd not like <cls name>.all() delegate to super().default()
        if cmd.endswith('.all()'):
            self.class_all(cmd.split('.')[0]) 
        elif cmd.endswith('.count()'):
            self.class_count(cmd.split('.')[0])
        elif self.is_class_dot_show(cmd):  # if it is classname.show() command
            self.class_dot_show(*self.parse_class_dot_show_args(cmd))
        elif self.is_class_dot_destroy(cmd):  # if is ClassName.destroy()
            self.class_dot_destroy(*self.parse_class_dot_destroy_args(cmd))
        else:
            super().default(line)

    def class_all(self, class_name):
        '''Gets all instances of class.'''
        if class_name in CLASSNAMES:
            _list = [
                str(obj) for key, obj in storage.all().items()
                if key.startswith(class_name)
                ]
            print(_list)
        else:
            super().default(class_name)
    
    def class_count(self, class_name):
        '''Count number of instances of a class.'''
        if class_name in CLASSNAMES:
            count = 0
            for key in storage.all():
                if key.startswith(class_name):
                    count += 1
            print(count)
        else:
            super().default(class_name)

    def class_dot_show(self, class_name, _id):
        '''Retrieve an instance based on its id.'''
        if class_name == '':
            print('** class name missing **')
        elif _id == '':
            print('** instance id missing **')
        else:
            search_key = '{}.{}'.format(class_name, _id)
            if search_key in storage.all():
                print(str(storage.all()[search_key]))
            else:
                print('** no instance found **')

    def parse_class_dot_show_args(self, cmd):
        '''Retrieve class name and id.
        From <class name>.show("id") like command.
        '''
        quote_1_idx = cmd.find('"')
        quote_2_idx = cmd.find('"', quote_1_idx + 1)
        _id = cmd[quote_1_idx + 1: quote_2_idx]
        class_name = cmd.split('.')[0]
        return class_name, _id

    def parse_class_dot_destroy_args(self, cmd):
        '''Retrieve class name and id.
        From <class name>.destroy("id") like command.
        '''
        quote_1_idx = cmd.find('"')
        quote_2_idx = cmd.find('"', quote_1_idx + 1)
        _id = cmd[quote_1_idx + 1: quote_2_idx]
        class_name = cmd.split('.')[0]
        return class_name, _id

    def class_dot_destroy(self, class_name, _id):
        '''Retrieve an instance based on its id.'''
        if class_name == '':
            print('** class name missing **')
        elif _id == '':
            print('** instance id missing **')
        else:
            search_key = '{}.{}'.format(class_name, _id)
            if search_key in storage.all():
                storage.all().pop(search_key)
                storage.save()
            else:
                print('** no instance found **')

    @staticmethod
    def is_class_dot_show(cmd):
        '''Determines if cmd is like <cls name>.show(id).'''

        if '.show(' in cmd and ')' in cmd:
            if cmd.count('(') == 1 and cmd.count(')') == 1:
                # -2 because the diff btwn '(' and ')' must be at least 2
                # to be valid like .show("") not .show()
                if cmd.index('(') < cmd.index(')') - 2:
                    if cmd.index(')') == len(cmd) - 1:
                        if cmd[cmd.index('(') + 1] == '"':
                            if cmd[cmd.index(')') - 1] == '"':
                                return True
        return False

    @staticmethod
    def is_class_dot_destroy(cmd):
        '''Determines if cmd is like <cls name>.destroy("id").'''

        if '.destroy(' in cmd and ')' in cmd:
            if cmd.count('(') == 1 and cmd.count(')') == 1:
                # -2 because the diff btwn '(' and ')' must be at least 2
                # to be valid like .destroy("") not .destroy()
                if cmd.index('(') < cmd.index(')') - 2:
                    if cmd.index(')') == len(cmd) - 1:
                        if cmd[cmd.index('(') + 1] == '"':
                            if cmd[cmd.index(')') - 1] == '"':
                                return True
        return False

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
