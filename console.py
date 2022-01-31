#!/usr/bin/env python3
'''AirBnB Console that interacts with data objects of the application.'''


import cmd
import models
from models import base_model, user, state, review, place, city, amenity
import json


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

    def do_create(self, cls_name):
        '''Creates a new instance of BaseModel, saves it and prints the id.'''
        if not cls_name:
            print('** class name missing **')
        elif cls_name not in CLASSNAMES:
            print('** class doesn\'t exist ** ')
        else:
            instance = CLASSNAMES[cls_name]()
            instance.save()
            print(instance.id)

    def do_show(self, args):
        '''Prints an instance based on class name and id.
        show <class name> <id>
        '''
        args = self.parse_args_2(args)
        if args is None:
            return
        cls_name, _id = args
        search_key = self.get_search_key(cls_name, _id)
        print(storage.all()[search_key])

    def do_destroy(self, args):
        '''Deletes an instance.

        Based on the class name and id.
        Saves changes to file.
        '''
        args = self.parse_args_2(args)
        if args is None:
            return
        cls_name, _id = args
        search_key = self.get_search_key(cls_name, _id)
        storage.all().pop(search_key)
        storage.save()

    def do_all(self, cls_name):
        '''Prints all instances based on or not on class name.
        all [<class name>]
        '''
        _list = []
        if not cls_name:
            for key, instance in storage.all().items():
                _list.append(str(instance))
            print(_list)
            return
        if cls_name in CLASSNAMES:
            for key, instance in storage.all().items():
                if key.startswith(cls_name):
                    _list.append(str(instance))
            print(_list)
        else:
            print('** class doesn\'t exist **')

    def do_update(self, args):
        '''Updates an instance based on class name and id.
        update <class name> <id> <attr> "<value>"
        '''
        args = self.parse_args_for_update(args)
        if args is None:
            return
        cls_name, _id, attr, value = args
        search_key = self.get_search_key(cls_name, _id)
        obj = self.find_obj(search_key)
        if obj is None:
            print('** no instance found **')
            return
        existing_attr = getattr(obj, attr, None)
        if existing_attr is None:
            setattr(obj, attr, value)
        else:
            _class = type(existing_attr)
            if _class is list:
                if value not in existing_attr:
                    tmp_list = list(existing_attr)
                    tmp_list.append(value)
                    setattr(obj, attr, tmp_list)
            else:
                value = _class(value)
                setattr(obj, attr, value)
        storage.save()

    def default(self, line):
        '''Handles commands like <cls name>.all().'''
        cmd = line.strip()

        # if cmd not like <cls name>.all() delegate to super().default()
        if cmd.endswith('.all()'):
            self.class_dot_all(cmd.split('.')[0])
        elif cmd.endswith('.count()'):
            self.class_dot_count(cmd.split('.')[0])
        elif self.is_class_dot_show(cmd):  # if it is classname.show() command
            self.class_dot_show()
        elif self.is_class_dot_destroy(cmd):  # if is ClassName.destroy()
            self.class_dot_destroy(cmd)
        elif self.is_class_dot_update(cmd):
            self.class_dot_update(cmd)
        else:
            super().default(line)

    def class_dot_all(self, cls_name):
        '''Gets all instances of class.'''
        if cls_name in CLASSNAMES:
            _list = [
                str(obj) for key, obj in storage.all().items()
                if key.startswith(cls_name)
                ]
            print(_list)
        else:
            super().default(cls_name)

    def class_dot_count(self, cls_name):
        '''Count number of instances of a class.'''
        if cls_name in CLASSNAMES:
            count = 0
            for key in storage.all():
                if key.startswith(cls_name):
                    count += 1
            print(count)
        else:
            super().default(cls_name)

    def class_dot_show(self, cmd):
        '''Retrieve an instance based on its id.'''
        cls_name, _id = self.parse_class_dot_show_args(cmd)
        if cls_name == '':
            print('** class name missing **')
        elif _id == '':
            print('** instance id missing **')
        else:
            search_key = '{}.{}'.format(cls_name, _id)
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
        cls_name = cmd.split('.')[0]
        return cls_name, _id

    def parse_class_dot_destroy_args(self, cmd):
        '''Retrieve class name and id.
        From <class name>.destroy("id") like command.
        '''
        quote_1_idx = cmd.find('"')
        quote_2_idx = cmd.find('"', quote_1_idx + 1)
        _id = cmd[quote_1_idx + 1: quote_2_idx]
        cls_name = cmd.split('.')[0]
        return cls_name, _id

    def class_dot_destroy(self, cls_name, _id):
        '''Destroys an instance based on its id.'''
        cls_name, _id = self.parse_class_dot_destroy_args(cmd)
        if cls_name == '':
            print('** class name missing **')
        elif _id == '':
            print('** instance id missing **')
        else:
            search_key = '{}.{}'.format(cls_name, _id)
            if search_key in storage.all():
                storage.all().pop(search_key)
                storage.save()
            else:
                print('** no instance found **')

    def class_dot_update(self, cmd):
        '''Handles ClassName.update() commands
        <class name>.update(<id>, <attribute name>, <attribute value>).
        '''
        parsed_data = self.parse_class_dot_update(cmd)
        if None in parsed_data:
            return super().default(cmd)
        if len(parsed_data) == 4:
            cls_name, _id, attr, value = parsed_data
            args = '{} {} {} "{}"'.format(cls_name, _id, attr, value)
            self.do_update(args)
        else:
            cls_name, _id, _dict = parsed_data
            self.update_with_dict(cls_name, _id, _dict)

    def update_with_dict(self, cls_name, _id, _dict):
        '''Update object within storage with a dictionary'''
        search_key = self.get_search_key(cls_name, _id)
        obj = self.find_obj(search_key)
        if obj is None:
            print('** no instance **')
        else:
            for attr, value in _dict.items():
                setattr(obj, attr, value)
        storage.save()

    def parse_class_dot_update(self, cmd):
        '''Parses
        ClassName.update(id, attribute_name, "attribute_value").
        ClassName.update(id, <dictionary representation>)
        '''
        line = cmd.replace('.', '%^', 1)  # replace
        line = line.split('%^')  # split by that chars
        cls_name = line[0]
        args = line[1].replace('update(', '').replace(')', '')
        num_commas = args.count(',')

        if '{' not in args and '}' not in args:
            if num_commas < 2:
                return cls_name, None, None, None
            elif num_commas == 2:
                _id, attr, value = args.split(',')[0:]
                _id = _id.strip()
                attr = attr.strip()
                value = value.strip().strip('"')
                return cls_name, _id, attr, value
        else:
            lbrace_idx, rbrace_idx = args.find('{'), args.find('}')
            first_comma_idx = args.find(',')
            if args[-1] == '}':
                args = args.replace(',', '%^', 1)  # replace 1st
                tmp = args.split('%^')
                _id = tmp[0].strip().strip('"')
                _dict = tmp[1].strip().replace('\'', '"')
                try:
                    _dict = json.loads(_dict)
                except:
                    _dict = None
                return cls_name, _id, _dict
        return None, None, None, None

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
    def is_class_dot_update(cmd):
        '''Checks if cmd is like any of the forms below.

        <class name>.update(<id>, <attr name>, <attr value>).
        <class name>.update(<id>, <dictionary representation>).
        '''

        if '.update(' in cmd and cmd[-1] == ')':
            if cmd.count('(') == 1 and cmd.count(')') == 1:
                if cmd.index('(') < cmd.index(')'):
                    if not cmd.startswith('.'):
                        return True
        return False

    @staticmethod
    def find_obj(key):
        return storage.all().get(key, None)

    def parse_args_for_update(self, args):
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
        cls_name, _id, attr = args[:3]
        start = line.find('"') + 1
        end = line.find('"', start)
        if start == 0 or end == -1:
            super().default(line)
            return
        else:
            value = line[start:end]

        if cls_name not in CLASSNAMES:
            print('** class doesn\'t exist **')
            return
        if HBNBCommand.get_search_key(cls_name, _id) not in storage.all():
            print('** no instance found **')
            return
        return cls_name, _id, attr, value

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
            cls_name, _id = args

        if cls_name not in CLASSNAMES:
            print('** class doesn\'t exist ** ')
            return
        search_key = HBNBCommand.get_search_key(cls_name, _id)
        if search_key not in storage.all():
            print('** no instance found **')
            return
        return cls_name, _id

    @staticmethod
    def get_search_key(cls_name, _id):
        '''Returns the Classname.id format key from the storage.'''
        return '{}.{}'.format(cls_name, _id)


def main():
    '''entry point into the interpreter and the logic.'''
    console = HBNBCommand()
    console.cmdloop()


if __name__ == '__main__':
    main()
