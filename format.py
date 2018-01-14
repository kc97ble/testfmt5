#!/usr/bin/env python2

class Format:
    
    def __init__(self, text, infix_fmt=''):
        assert text.count('*') == 1
        i = text.index('*')
        self.prefix = text[:i]
        self.suffix = text[i+1:]
        self.infix_fmt = infix_fmt
    
    def __repr__(self):
        return "format.Format('{}*{}', '{}')".format(self.prefix, self.suffix, self.infix_fmt)
    
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
        infix = self.format_infix(infix, self.infix_fmt, index=index)
        return self.prefix + infix + self.suffix
'''
class FormatOld:
    
    def __init__(self, text):
        if '*' not in text:
            self.starred = False
            self.prefix = text
            self.suffix = ''
        else:
            assert text.count('*') == 1
            i = text.index('*')
            self.starred = True
            self.prefix = text[:i]
            self.suffix = text[i+1:]
    
    def __repr__(self):
        return "format.Format('{}{}{}')".format(self.prefix, 
            '*' if self.starred else '', self.suffix)
    
    def match(self, text):
        if not self.starred:
            return text == self.prefix
        return (len(self.prefix) + len(self.suffix) <= len(text) 
                and text.startswith(self.prefix)
                and text.endswith(self.suffix))
    
    def infix(self, text):
        assert self.match(text)
        if not self.starred:
            return ''
        return text[len(self.prefix) : len(text) - len(self.suffix)]
    
    def text(self, infix):
        if not self.starred:
            return self.prefix
        return self.prefix + infix + self.suffix
'''

def convert_format(text, fmt1, fmt2, index=0):
    infix = fmt1.infix(text)
    return fmt2.text(infix, index)

def convert_format_list(items, fmt1, fmt2):
    return [convert_format(items[i], fmt1, fmt2, i) for i in range(len(items))]
    
if __name__ == '__main__':
    print Format('t*.in')
    print Format('t*.in').match('t1.in')
    print Format('t*.in').match('t.in')
    print Format('a*a').match('aaa')
    print Format('a*a').match('aa')
    print Format('a*a').match('a')
    print Format('t*.in').infix('t1.in')
    print Format('t*.in').infix('t.in')
    print Format('a*a').infix('aaa')
    print Format('a*a').infix('aa')
    print Format('a*a').text('aa')
    print Format('a*a').text('bb')
    
    
