#!/usr/bin/env python3.3
from pyawk import PyAwk, p
def decorate_action(method):
    def wrapper(self, *args):
        self.print('decorate_action start')
        method(self, *args)
        self.print('decorate_action finish')
        self.print()
    return wrapper

class Decorator(PyAwk):
    @decorate_action
    def begin(self):
        self.print('begin method')

    @decorate_action
    def begin_file(self):
        self.print('begin file method')

    @decorate_action
    def action(self, S):
        self.print(S[1:])

    @decorate_action
    def end_file(self):
        self.print('end file method')

    @decorate_action
    def end(self):
        self.print('end method')

if __name__ == '__main__':
    Decorator().run()
