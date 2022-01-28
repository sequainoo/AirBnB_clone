#!/usr/bin/env python3
'''AirBnB Console that interacts with data objects of the application.'''


import cmd
import models


CLASSNAMES = {
    'BaseModel': models.base_model.BaseModel
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
        '''Prints the str representation of an instance based on class name and id.'''
        args =  self.parse_args_2(args)
        if args is None:
            return
        class_name, _id = args
        search_key = key_from_storage(class_name, _id)
        print(storage.all()[search_key])
    
    def do_destroy(self, args):
        '''Deletes an instance based on the class name and id, saves changes to file.'''
        args =  self.parse_args_2(args)
        if args is None:
            return
        class_name, _id = args
        search_key = key_from_storage(class_name, _id)
        storage.all().pop(search_key)
        storage.save()
    
    def do_all(self, class_name):
        '''Prints str representation of all instances based on or not on class name.'''
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
        search_key = HBNBCommand.key_from_storage(class_name,_id)
        if not search_key in storage.all():
            print('** no instance found **')
            return
        return class_name, _id

    @staticmethod
    def key_from_storage(class_name, _id):
        '''Returns the Classname.id format key from the storage.'''
        return '{}.{}'.format(class_name,_id)


def main():
    '''entry point into the interpreter and the logic.'''
    console = HBNBCommand()
    console.cmdloop()


if __name__ == '__main__':
    main()
