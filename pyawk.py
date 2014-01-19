import sys
import re
class PyAwk(object):
    def __init__(self):
        self.PATTERN_METHOD_PREFIX = 'pat' # Prefix of pattern method
        self.FS = '[ \t+]' # Field separator
        self.FILENAME = '' # File name
        self.NF = 0 # Number of fields
        self.NR = 0 # Number of records
        self.FNR = 0 # File number of records

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

    def run(self):
        '''Run PyAwk'''
        # Call begin method
        begin_method = getattr(self, 'begin', None)
        if begin_method != None and callable(begin_method):
            begin_method()

        # Set input type
        if len(sys.argv) == 1:
            input_lines = sys.stdin
            self.__each_line(input_lines)
        else:
            del sys.argv[0:1]
            for file_name in sys.argv:
                with open(file_name) as input_lines:
                    self.FILENAME = file_name
                    self.__each_line(input_lines)

        # Call end method
        end_method = getattr(self, 'end', None)
        if end_method != None and callable(end_method):
            end_method()

    def __each_line(self, input_lines):
        '''Process each line'''
        self.FNR = 0
        # Read lines
        for line in input_lines:
            self.NR = self.NR + 1
            self.FNR = self.FNR + 1
            stripped_line = line.strip()
            columns = re.split(self.FS, stripped_line)
            self.NF = len(columns) if stripped_line else 0
            columns.insert(0, stripped_line)

            # Call each pattern
            patterns = [ name for name in dir(self.__class__) if name.startswith(self.PATTERN_METHOD_PREFIX) ]
            for pattern in patterns:
                method = getattr(self, pattern, None)
                if method != None and callable(method):
                    method(columns)

if __name__ == '__main__':
    from doctest import testmod
    testmod()
