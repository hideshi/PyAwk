import sys
import os
import re
class PyAwk(object):
    def __init__(self):
        self.ACTION_METHOD_PREFIX = 'act' # Prefix of action method
        self.FILENAME = '' # File name
        self.FS = '[ \t+]' # Field separator
        self.OFS = ' ' # Output field separator
        self.RS = os.linesep # Record separator
        self.ORS = os.linesep # Output record separator
        self.NF = 0 # Number of fields
        self.NR = 0 # Number of records
        self.FNR = 0 # File number of records

    def run(self):
        '''Run PyAwk'''
        # Call begin method
        begin_method = getattr(self, 'begin', None)
        if begin_method != None and callable(begin_method):
            begin_method()

        # Set input type
        if len(sys.argv) == 1:
            f = sys.stdin
            self.__each_line(f)
        else:
            for file_name in sys.argv[1:]:
                with open(file_name, newline=self.RS) as f:
                    self.FILENAME = file_name
                    self.__each_line(f)

        # Call end method
        end_method = getattr(self, 'end', None)
        if end_method != None and callable(end_method):
            end_method()

    def __each_line(self, f):
        '''Process each line'''
        self.FNR = 0
        # Read lines
        for line in f:
            self.NR = self.NR + 1
            self.FNR = self.FNR + 1
            stripped_line = line.strip()
            columns = re.split(self.FS, stripped_line)
            self.NF = len(columns) if stripped_line else 0
            columns.insert(0, stripped_line)

            # Call each action
            actions = [ name for name in dir(self.__class__) if name.startswith(self.ACTION_METHOD_PREFIX) ]
            for action in actions:
                action_method = getattr(self, action, None)
                if action_method != None and callable(action_method):
                    action_method(columns)

    def p(self, string, pattern):
        '''
        Pattern matcher
        >>> PyAwk().p('Python3', r'^[A-Z]\w{5}')
        True
        >>> PyAwk().p('Python3', r'[a-z]\d$')
        True
        >>> PyAwk().p('Python3', r'^\w.*\s.*\d$')
        False
        '''
        p = re.compile(pattern)
        return True if p.search(string) != None else False

    def print(self, *args):
        '''
        >>> PyAwk().print('Python3')
        Python3
        >>> PyAwk().print('Python3', 'awk')
        Python3 awk
        '''
        string = self.OFS.join(args)
        print(string, end=self.ORS)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
