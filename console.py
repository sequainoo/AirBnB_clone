#!/usr/bin/env python3
'''AirBnB Console that interacts with data objects of the application.'''


import cmd
import sys
import os


class BashCLI(cmd.Cmd):
    '''Interprets bash commands.

    bash python3 -m unittest discover tests
    '''

    def do_bash(self, line):
        '''
        Execute bash/shell commands.
        Usage:
            bash [cmdname] [-optionflags] [parameter [...]]
        
        Example:
            bash python3 -m unittest discover tests
        '''
        if line:
            os.system(line)
    

class Console(BashCLI):
    prompt = '(hbnb) '
    # intro = ' .---------------------------.\n'
    # intro += '|    Welcome to hbnb CLI!     |\n'
    # intro += '|    for help, input `help`   |\n'
    # intro += '|    for quit, input `quit`   |\n'
    # intro += ' `---------------------------`\n'
    
    def do_quit(self, inp):
        '''Quit the console ((hbnb) quit)'''
        # print()
        return True

    def do_EOF(self, inp):
        '''Handles EOF signal.'''
        return self.do_quit(inp)
    

    

    


def main():
    if len(sys.argv) > 1:
        # run in non interactive mode
        string = ' '.join(sys.argv[1:])
        Console().onecmd(string)
    else:
        # run in interactive mode
        Console().cmdloop()

if __name__ == '__main__':
    main()
