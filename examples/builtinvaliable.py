#!/usr/local/bin/python3.3
from pyawk import PyAwk
class BuiltInValiable(PyAwk):
    def begin(self):
        self.FS = ','
        self.OFS = '\t'
        self.RS = '\n'
        self.ORS = '\r\n'

    def action(self, S):
        self.print(S[1], S[2], S[3])

if __name__ == '__main__':
    BuiltInValiable().run()
