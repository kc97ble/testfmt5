#!/usr/bin/env python2

class Format:
    
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

def convert_format(text, fmt1, fmt2):
    infix = fmt1.infix(text)
    return fmt2.text(infix)

def convert_format_list(items, fmt1, fmt2):
    return [convert_format(x, fmt1, fmt2) for x in items]
    
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
    
    
