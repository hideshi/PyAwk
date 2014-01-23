#!/usr/bin/env python3.3
from pyawk import PyAwk
class CSVtoTSV(PyAwk):
    def begin(self):
        self.FS = '\s*,\s*'

    def action(self, S):
        self.print('\t'.join(S[1:]))

if __name__ == '__main__':
    CSVtoTSV().run()
