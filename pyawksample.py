#!/usr/local/bin/python3.3
from pyawk import PyAwk
class PyAwkSample(PyAwk):
    def begin(self):
        self.count = 0
        self.current_file_name = ''

    def action1(self, S):
        self.count = self.count + 1 
        if self.FILENAME != self.current_file_name:
            print('FILENAME', self.FILENAME)
            self.current_file_name = self.FILENAME
        print(str(self.FNR) + '\t' + S[self.NF])

    def action2(self, S):
        if len(S) >= 10 and self.p(S[9], r'\.py'):
            print(S[9])

    def end(self):
        print('FS', '"' + self.FS + '"')
        print('NR', self.NR)
        print(self.count, 'lines')

if __name__ == '__main__':
    PyAwkSample().run()
