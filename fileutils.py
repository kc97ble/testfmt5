#!/usr/bin/env python2

class FileList:
    
    def __init__(self, files, real=False):
        self.real = real
        self.files = files
    
    def __repr__(self):
        return 
    
    def really_renames(self, src, dst):
        """ (self, str, str) -> bool """
        try:
            os.renames(src, dst)
        except OSError:
            return False
        return True
    
    def move_file(self, src, dst):
        """ (self, str, str) -> bool """
        if src == dst:
            return src in self.files
        if (src not in self.files) or (dst in self.files):
            return False
        print "Moving '{}' -> '{}'".format(src, dst)
        self.files[self.files.index(src)] = dst
        return really_renames(self, src, dst) if real else True
    
if __name__ == '__main__':
    print FileList(['a', 'b', 'c'])
    
    
'''    

def move_file(src, dst):
    """ (str, str) -> bool (True for success, False otherwise) """
    if is_testing:
        if dst in testing_file_list:
            return False
        if src not in testing_file_list:
            return False
        testing_file_list[testing_file_list.index(src)] = dst
        print "'{}' -> '{}'".format(src, dst)
        return True
    
    else:
        if os.path.exists(dst):
            return False
        try:
            os.renames(src, dst)
        except OSError:
            return False
        return True

def move_files_best_effort(src, dst):
    """ (list, list) -> int (number of successes) """
    assert len(src) == len(dst)
    n = len(src)
    
    for i in range(n):
        if move_file(src[i], dst[i]) == False:
            return i
    return n

def move_files_directly(src, dst):
    """ (list, list) -> int
    Returns
        0 for success
        1 for failed but recovered
        2 for failed but not recovered
    """
    
    assert len(src) == len(dst)
    n = len(src)
    
    success = move_files_best_effort(src, dst)
    if success == n:
        return 0
    else:
        src2 = reversed(dst[:success])
        dst2 = reversed(src[:success])
        recovered = move_files_best_effort(src2, dst2)
        if recovered == success:
            return 1
        else:
            return 2

def move_files_indirectly(src, dst):
    assert len(src) == len(dst)
    n = len(src)
    pre = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    sep = '--------'
    mid = range(n)
    
    for i in range(n):
        t0 = src[i].replace('/', '----').replace('\\', '------')
        t1 = dst[i].replace('/', '----').replace('\\', '------')
        mid[i] = pre+sep+t0+sep+t1+sep+str(i).zfill(8)+'.testdata'
    
    return move_files_directly(src+mid, mid+dst)
    
def get_file_dirr_list(path):
    try:
        found = [os.path.join(path, x) for x in os.listdir(path)]
    except OSError:
        found = []
        
    files = [x for x in found if os.path.isfile(x)]
    dirrs = [x for x in found if os.path.isdir(x)]
    return (files, dirrs)

def get_file_list(depth=2):
    curr = ['.']
    succ = []
    rslt = []
    
    for i in range(depth):
        for path in curr:
            (files, dirrs) = get_file_dirr_list(path)
            succ.extend(dirrs)
            rslt.extend(files)
        curr = succ
        succ = []
    return rslt
'''
