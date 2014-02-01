#!/usr/bin/env python3.3
from pyawk import PyAwk, p
class FixedLength(PyAwk):
    def begin(self):
        self.FIELDWIDTHS = [6,2,4]

    def action(self, S):
        print(S[0], S[1], S[2], S[3])

if __name__ == '__main__':
    FixedLength().run()
