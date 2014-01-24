#!/usr/bin/env python3.3
from pyawk import PyAwk, p
class SQLite(PyAwk):
    def begin(self):
        # if SQL statement sets on self.QUERY
        # and file name ends with '.db', 
        # database will be searched.
        self.QUERY = 'select * from test'

    def action(self, S):
        if self.NR == 1:
            self.print(self.FILENAME)
        self.print(S[1], S[self.NF])

    def end(self):
        self.print(self.NR)

if __name__ == '__main__':
    SQLite().run()
