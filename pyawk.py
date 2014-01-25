import sys
import os
import re
import argparse
import sqlite3

def _debugger(action_method):
    def wrapper(self, columns = None):
        if self._args.debug:
            self.print('++')
            self.print('++', columns, getattr(self, '__dict__', None))
            self.print('++')

        if columns:
            action_method(columns)
        else:
            action_method()
    return wrapper

def p(string, pattern):
    '''
    Pattern matcher
    >>> p('Python3', r'^[A-Z]\w{5}')
    True
    >>> p('Python3', r'[a-z]\d$')
    True
    >>> p('Python3', r'^\w.*\s.*\d$')
    False
    '''
    p = re.compile(pattern)
    return True if p.search(string) != None else False

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
        self.QUERY = '' # SQL statement

    def run(self):
        '''Run PyAwk'''
        # Parse arguments
        parser = argparse.ArgumentParser(description='Process arguments')
        parser.add_argument('-d', '--debug', help='enable debug mode', action='store_true')
        parser.add_argument('-v', metavar='valiables', help='set valiables key=value[,key=value ...]')
        parser.add_argument('files', metavar='file', nargs='*', help='input file')
        self._args = parser.parse_args()

        if self._args.v:
            valiables = self._args.v.split(',')
            for v in valiables:
                key, value = v.split('=')
                setattr(self, key, value)

        # Call begin method
        begin_method = getattr(self, 'begin', None)
        if begin_method != None and callable(begin_method):
            begin_method()

        # Set input type
        if len(self._args.files) == 0:
            f = sys.stdin
            self.__call_begin_file_method()
            self.__process_each_line(f)
            self.__call_end_file_method()
        else:
            for file_name in self._args.files[0:]:
                try:
                    self.FILENAME = file_name
                    self.__call_begin_file_method()

                    if file_name.endswith('.db'):
                        conn = sqlite3.connect(file_name)
                        with conn:
                            cursor = conn.cursor()
                            self.__process_each_line(cursor.execute(self.QUERY).fetchall())
                    else:
                        with open(file_name, newline=self.RS) as f:
                            self.__process_each_line(f)

                    self.__call_end_file_method()

                except (IOError, sqlite3.OperationalError) as e:
                    sys.stderr.write(str(e) + '\n')
                    sys.exit(1)

        # Call end method
        end_method = getattr(self, 'end', None)
        if end_method != None and callable(end_method):
            end_method()

    def __call_begin_file_method(self):
        '''Call begin_file method'''
        begin_file_method = getattr(self, 'begin_file', None)
        if begin_file_method != None and callable(begin_file_method):
            wrapped_method = _debugger(begin_file_method)
            wrapped_method(self)

    def __call_end_file_method(self):
        '''Call end_file method'''
        end_file_method = getattr(self, 'end_file', None)
        if end_file_method != None and callable(end_file_method):
            wrapped_method = _debugger(end_file_method)
            wrapped_method(self)

    def __process_each_line(self, f):
        '''Process each line'''
        self.FNR = 0
        # Read lines
        for line in f:
            self.NR = self.NR + 1
            self.FNR = self.FNR + 1
            if isinstance(line, tuple):
                columns = list(line)
                self.NF = len(columns)
                columns.insert(0, line)
            else:
                stripped_line = line.strip()
                columns = re.split(self.FS, stripped_line)
                self.NF = len(columns) if stripped_line else 0
                columns.insert(0, stripped_line)

            # Call each action
            actions = [ name for name in dir(self.__class__) if name.startswith(self.ACTION_METHOD_PREFIX) ]
            for action in actions:
                action_method = getattr(self, action, None)
                if action_method != None and callable(action_method):
                    wrapped_method = _debugger(action_method)
                    wrapped_method(self, columns)

    def print(self, *args):
        '''
        >>> PyAwk().print('Python3')
        Python3
        >>> PyAwk().print('Python3', 'awk')
        Python3 awk
        '''
        print(*args, sep=self.OFS, end=self.ORS)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
