#!/usr/bin/env python2

""" filelist.py

BaseFileList
FileList
ZipFileList

Usage:
    file_list = FileList/ZipFileList(...)
    print file_list.files
    file_list.files = ...
    success = file_list.move_files_indirectly(src, dst, real=..., quiet=...)
"""

import os
import sys
import zipfile
import datetime

import misc

from zipfile import ZipFile

class BaseFileList(object):
    """
    Moves files.
    
    Properties:
        files (list)
    
    Methods:
        __init__(self, files)
        __repr__(self):
        really_renames(self, src, dst)
        move_file(self, src, dst, real=False, quiet=False)
        move_files_best_effort(self, src, dst, **kwargs)
        move_files_directly(self, src, dst, **kwargs)
        move_files_indirectly(self, src, dst, **kwargs)
    """
    
    def __init__(self, files):
        self.files = list(files)
    
    def __repr__(self):
        return 'filelist.BaseFileList({})'.format(self.files)
    
    def really_renames(self, src, dst):
        """ (self, str, str) -> bool """
        raise NotImplementedError

    def move_file(self, src, dst, real=False, quiet=False):
        """ (self, str, str, ...) -> bool
        
        Moves a file.
        
        Changes:
            self.files
            really_renames will be called if self.real == True
        Returns:
            True if success,
            False otherwise.
        """
        if src == dst:
            return src in self.files
        if (src not in self.files) or (dst in self.files):
            return False
        if not quiet:
            print "Moving '{}' -> '{}'".format(src, dst)
        self.files[self.files.index(src)] = dst
        return self.really_renames(src, dst) if real else True
        
    def move_files_best_effort(self, src, dst, **kwargs):
        """ (list, list) -> int
        
        Moves files, stop at the first failure.
        
        Returns:
            Number of successful moves
        """
        assert len(src) == len(dst)
        n = len(src)
        
        for i in range(n):
            if not self.move_file(src[i], dst[i], **kwargs):
                return i
        return n
    
    def move_files_directly(self, src, dst, **kwargs):
        """ (self, list, list) -> bool
        
        Moves files. If success, returns True.
        Otherwise, recovers the original state and return False.
        Exceptions will be raised if recovering is failed.
        
        Returns:
            True if success,
            False otherwise.
        """
        assert len(src) == len(dst)
        n = len(src)
        
        success = self.move_files_best_effort(src, dst, **kwargs)
        if success == n:
            return True
        else:
            src2 = list(reversed(dst[:success]))
            dst2 = list(reversed(src[:success]))
            recovered = self.move_files_best_effort(src2, dst2, **kwargs)
            if recovered == success:
                return False
            else:
                raise RuntimeError("Failed to recover")
    
    def move_files_indirectly(self, src, dst, **kwargs):
        """ (self, list, list, ...) -> bool
        
        Same as move_file_directly, except that this method 
        uses an intermediate list of file names to move files.
        
        Returns:
            True if success,
            False otherwise.
        """
        
        n = misc.ensure_equal_len(src, dst)
        pre = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        sep = '--------'
        mid = range(n)
        
        for i in range(n):
            t0 = src[i].replace('/', '----').replace('\\', '------')
            t1 = dst[i].replace('/', '----').replace('\\', '------')
            mid[i] = pre+sep+t0+sep+t1+sep+str(i).zfill(8)+'.testdata'

        return self.move_files_directly(src+mid, mid+dst, **kwargs)

class FileList(BaseFileList):
    """
    Moves files in the working directory.
    """
    
    @classmethod
    def from_working_directory(cls, **kwargs):
        return cls(misc.get_file_list_recursively(**kwargs))
        
    def really_renames(self, src, dst):
        """ (self, str, str) -> bool """
        try:
            os.renames(src, dst)
        except OSError as e:
            print >> sys.stderr, e.errno
            print >> sys.stderr, e
            return False
        return True

class ZipFileList(BaseFileList):
    
    """
    Moves files in a ZIP file.
    """
    
    def __init__(self, zip_path):
        self.src_path = zip_path
        files = ZipFile(self.src_path, 'r').namelist()
        super(ZipFileList, self).__init__(files)
  
    def really_renames(self, src, dst):
        if src == dst:
            return True
        if (dst in self.old_name) or (src not in self.old_name):
            return False
        self.old_name[dst] = self.old_name.pop(src)
        return True
    
    def apply_changes(self, quiet=False):
        src_path = self.src_path
        dst_path = src_path + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        try:
            with ZipFile(src_path, 'r') as src, ZipFile(dst_path, 'w', zipfile.ZIP_DEFLATED) as dst:
                assert src.testzip() == None
                for name in self.old_name:
                    if not quiet:
                        print "Writing data of '{}'".format(name)
                    data = src.read(self.old_name[name])
                    info = src.getinfo(self.old_name[name])
                    info.filename = name
                    dst.writestr(info, data)
            
            assert ZipFile(dst_path, 'r').testzip() == None
            os.rename(src_path, dst_path + '.backup')
            os.rename(dst_path, src_path)
            os.remove(dst_path + '.backup')
        finally:
            if os.path.isfile(dst_path):
                os.remove(dst_path)
            if not os.path.isfile(src_path) and os.path.isfile(dst_path + '.backup'):
                os.rename(dst_path + '.backup', src_path)
    
    def move_files_directly(self, src, dst, **kwargs):
        self.old_name = {x: x for x in self.files}
        super(ZipFileList, self).move_files_directly(src, dst, **kwargs)
        if kwargs.get('real', False):
            self.apply_changes()
        del self.old_name
        return True
    
if __name__ == '__main__':
    print BaseFileList(['a', 'b', 'c'])
    assert BaseFileList(['a', 'b', 'c']).move_file('a', 'a', quiet=True) == True
    assert BaseFileList(['a', 'b', 'c']).move_file('a', 'b', quiet=True) == False
    assert BaseFileList(['a', 'b', 'c']).move_file('a', 'c', quiet=True) == False
    assert BaseFileList(['a', 'b', 'c']).move_file('a', 'd', quiet=True) == True
    assert BaseFileList(['a', 'b', 'c']).move_files_best_effort(['a', 'b'], ['d', 'e'], quiet=True) == 2
    assert BaseFileList(['a', 'b', 'c']).move_files_best_effort(['a', 'b'], ['d', 'd'], quiet=True) == 1
    assert BaseFileList(['a', 'b', 'c']).move_files_directly(['a', 'b'], ['d', 'e'], quiet=True) == True
    assert BaseFileList(['a', 'b', 'c']).move_files_directly(['a', 'b'], ['d', 'd'], quiet=True) == False
    assert BaseFileList(['a', 'b', 'c']).move_files_directly(['a', 'b', 'c'], ['c', 'd', 'e'], quiet=True) == False
    assert BaseFileList(['a', 'b', 'c']).move_files_indirectly(['a', 'b', 'c'], ['c', 'd', 'e'], quiet=True) == True
