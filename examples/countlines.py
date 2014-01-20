#!/usr/bin/env python
from pyawk import PyAwk
class CountLines(PyAwk):
    def end(self):
        print(self.NR)

if __name__ == '__main__':
    CountLines().run()
