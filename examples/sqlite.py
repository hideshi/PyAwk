#!/usr/bin/env python3.3
from pyawk import PyAwk, p
class SQLite(PyAwk):
    def begin(self):
        # if SQL statement sets on self.QUERY
        # and file name ends with '.db', 
        # database will be searched.
        self.QUERY = 'select * from test'
        self.OFS = ','

    def action(self, S):
        self.print(self.OFS.join(str(i) for i in S[1:]))

    def end(self):
        self.print(self.NR)

if __name__ == '__main__':
    SQLite().run()
