#!/usr/bin/env python3.3
from pyawk import PyAwk, p
class Template(PyAwk):
    def begin(self):
        pass

    def begin_file(self):
        pass

    def action(self, S):
        pass

    def end_file(self):
        pass

    def end(self):
        pass

if __name__ == '__main__':
    Template().run()
