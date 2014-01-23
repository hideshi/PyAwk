#!/usr/bin/env python3.3
from pyawk import PyAwk
class BuiltInValiable(PyAwk):
    def begin(self):
        self.FS = ','
        self.OFS = '\t'
        self.RS = '\n'
        self.ORS = '\r\n'

    def action(self, S):
        if self.FNR == 1:
            print(self.FILENAME)
        self.print(str(self.FNR), str(self.NR), S[1], S[self.NF])

if __name__ == '__main__':
    BuiltInValiable().run()
