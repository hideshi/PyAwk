#!/usr/bin/env python3.3
from pyawk import PyAwk
class LTSVParser(PyAwk):
    def begin(self):
        self.FS = '\t'

    def action(self, S):
        self.print('----------')
        d = {}
        for elem in S:
            key, value = elem.split(':', 1)
            d[key] = value
        self.print(d)

    def end(self):
        self.print('----------')
        self.print('TOTAL:{}'.format(self.NR))

if __name__ == '__main__':
    LTSVParser().run()
