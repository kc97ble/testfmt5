#!/usr/bin/env python3

import format
from functools import total_ordering

class FormatPair:
    
    def __init__(self, ifmt, ofmt):
        assert isinstance(ifmt, format.Format)
        self.ifmt = ifmt
        self.ofmt = ofmt
    
    @classmethod
    def from_string(cls, text):
        assert text.count('|') == 1
        istr, ostr = text.split('|')
        ifmt = format.Format.from_string(istr)
        ofmt = format.Format.from_string(ostr)
        return FormatPair(ifmt, ofmt)
    
    def __repr__(self):
        return 'FormatPair(%s, %s)' % (self.ifmt, self.ofmt)
    
    def __str__(self):
        return '(%s, %s)' % (str(self.ifmt), str(self.ofmt))
    
    def __eq__(this, that):
        return this.__dict__ == that.__dict__
    
ALL_KNOWN_FORMAT_PAIRS = list(map(FormatPair.from_string, [
    '*|*.a',
    '*.in|*.ok',
    '*.inp|*.out',
    '*.in|*.out',
    '*.in|*.ans',
    '*.in|*.a',
    'debug.in.*|debug.out.*',
    'in.*|ans.*',
]))

DEFAULT_IFMT = format.Format.from_string('*00*.in')
DEFAULT_OFMT = format.Format.from_string('*00*.ok')

if __name__ == '__main__':
    print(ALL_KNOWN_FORMAT_PAIRS)
    print(map(str, ALL_KNOWN_FORMAT_PAIRS))
    assert FormatPair.from_string('*|*') == FormatPair.from_string('*|*')
    assert FormatPair.from_string('*|*') != FormatPair.from_string('*|*.a')
