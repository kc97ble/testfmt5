#!/usr/bin/env python3

class Format:
    
    def __init__(self, prefix, inffmt, suffix):
        self.prefix = prefix
        self.inffmt = inffmt
        self.suffix = suffix
    
    @classmethod
    def from_string(self, text):
        assert text.count('*') in (1, 2)
        ll, rr = text.index('*'), text.rindex('*')
        prefix, suffix = text[:ll], text[rr+1:]
        inffmt = '' if ll==rr else text[ll+1:rr]
        return Format(prefix, inffmt, suffix)
    
    def __repr__(self):
        return 'Format(%s)' % self.__dict__
    
    def __str__(self):
        if self.inffmt == '':
            return "{}*{}".format(self.prefix, self.suffix)
        return "{}*{}*{}".format(self.prefix, self.inffmt, self.suffix)
    
    def __eq__(this, that):
        return this.__dict__ == that.__dict__
    
    def __ne__(this, that):
        return this.__dict__ != that.__dict__
    
    def match(self, text):
        return (len(self.prefix) + len(self.suffix) <= len(text) 
                and text.startswith(self.prefix)
                and text.endswith(self.suffix))
    
    def infix(self, text):
        assert self.match(text)
        return text[len(self.prefix) : len(text) - len(self.suffix)]
        
    def format_infix(self, infix, fmt, index=0):
        if fmt == '':
            return infix
        elif fmt in ['0', '1', '00', '01', '000', '001', '0000', '0001']:
            return str(index + int(fmt[-1]=='1')).zfill(len(fmt))
        else:
            raise NotImplementedError
    
    def text(self, infix, index=0):
        infix = self.format_infix(infix, self.inffmt, index=index)
        return self.prefix + infix + self.suffix

def convert_format(text, fmt1, fmt2, index=0):
    infix = fmt1.infix(text)
    return fmt2.text(infix, index)

def convert_format_list(items, fmt1, fmt2):
    return [convert_format(items[i], fmt1, fmt2, i) for i in range(len(items))]
    
if __name__ == '__main__':
    print(Format.from_string('t*.in'))
    print(Format.from_string('t*.in').match('t1.in'))
    print(Format.from_string('t*.in').match('t.in'))
    print(Format.from_string('a*a').match('aaa'))
    print(Format.from_string('a*a').match('aa'))
    print(Format.from_string('a*a').match('a'))
    print(Format.from_string('t*.in').infix('t1.in'))
    print(Format.from_string('t*.in').infix('t.in'))
    print(Format.from_string('a*a').infix('aaa'))
    print(Format.from_string('a*a').infix('aa'))
    print(Format.from_string('a*a').text('aa'))
    print(Format.from_string('a*a').text('bb'))
    
    
