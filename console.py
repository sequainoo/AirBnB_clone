#!/usr/bin/env python3
'''AirBnB Console that interacts with data objects of the application.'''


import cmd


class HBNBCommand(cmd.Cmd):
    '''The Console'''

    prompt = '(hbnb) '

    def do_quit(self, inp):
        '''
        Quits the console.
        Usage: quit
        '''
        return True

    def do_EOF(self, inp):
        '''
        Quits the console.
        Usage: ctrl + d.
        '''
        return True


def main():
    '''entry point into the interpreter and the logic.'''
    console = HBNBCommand()
    console.cmdloop()


if __name__ == '__main__':
    main()
