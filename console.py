#!/usr/bin/env python3
'''AirBnB Console that interacts with data objects of the application.'''


import cmd
import models


CLASSNAMES = {
    'BaseModel': models.base_model.BaseModel
}


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


    # @staticmethod
    # def alert_invalid_input(class_name):
    #     '''Prints error message on invalid arguments.'''

    # @staticmethod
    # def exists(class_name, _id):
    #     '''Checks for existence of instance with id and class name.'''
    #     pass


def main():
    '''entry point into the interpreter and the logic.'''
    console = HBNBCommand()
    console.cmdloop()


if __name__ == '__main__':
    main()
