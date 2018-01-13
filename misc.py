#!/usr/bin/env python2

import os

def ensure_equal_len(lst, *args):
    """ (list, ...) -> int
    
    Checks if all lists have the same length and returns the length.
    
    """
    n = len(lst)
    for x in args:
        assert len(x) == n
    return n

def get_file_list_and_dirr_list(path):
    """ (str) -> (list, list)
    
    List all files and directories DIRECTLY inside a path.
    """
    try:
        found = os.listdir(path)
        if path != '.':
            found = [os.path.join(path, x) for x in found]
    except OSError:
        found = []
        
    files = [x for x in found if os.path.isfile(x)]
    dirrs = [x for x in found if os.path.isdir(x)]
    return (files, dirrs)

def get_file_list_recursively(depth=2):
    """ (...) -> list
    
    List all files recursively.
    """
    curr = ['.']
    succ = []
    rslt = []
    
    for i in range(depth):
        for path in curr:
            (files, dirrs) = get_file_list_and_dirr_list(path)
            succ.extend(dirrs)
            rslt.extend(files)
        curr = succ
        succ = []
    return list(sorted(rslt))

def join_alternatively(lst1, lst2):
    """ (list, list) -> list
    
    Returns (lst1[0], lst2[0], lst1[1], lst2[1], ...)
    
    """
    n = ensure_equal_len(lst1, lst2)
    rslt = []
    for i in range(n):
        rslt.append(lst1[i])
        rslt.append(lst2[i])
    return rslt

def output_detect_result(ifiles, ofiles, is_simple=False):
    """
    Print ifiles and ofiles under the following formats.

    Simple format:
        1.inp
        1.out
        2.inp
        2.out

    Normal format:
        '1.inp', '1.out'
        '2.inp', '2.out'

        Number of test case(s): 2.
    """
    n = ensure_equal_len(ifiles, ofiles)
    if is_simple:
        for i in range(n):
            print ifiles[i]
            print ofiles[i]
    else:
        for i in range(n):
            print "'{}', '{}'".format(ifiles[i], ofiles[i])

        if n==0:
            print "No test cases have been found."
        else:
            print ""
            print "Number of test case(s): {}.".format(n)

def output_src_and_dst(src, dst, is_simple=False):
    """ (list, list) -> None

    Prints src and dst using the following formats.

    Simple format:
        1.inp
        1.in
        1.out
        1.ok
        2.inp
        2.in
        2.out
        2.ok

    Normal format:
        '1.inp' -> '1.in'
        '1.out' -> '1.ok'
        '2.inp' -> '2.in'
        '2.out' -> '2.ok'

    """
    n = ensure_equal_len(src, dst)
    if is_simple:
        for i in range(n):
            print src[i]
            print dst[i]
    else:
        for i in range(n):
            print "'{}' -> '{}'".format(src[i], dst[i])

def output_preview_result(success, num_test_cases, is_simple=False):
    """
    Display relevant information after previewing.
    """
    if is_simple:
        return
    print ""
    print "Number of test case(s): {}".format(num_test_cases)
    if success:
        print "OK. All tests passed."
    else:
        print "FAILED. Some test failed."
    print "Because of the preview mode, no file operations have been "\
        "performed, the test data has not been changed."

def output_convert_result(success, num_test_cases, is_simple=False):
    """
    Display relevant information after converting.
    """
    if is_simple:
        return
    print ""
    print "Number of test case(s): {}.".format(num_test_cases)
    if success:
        print "OK. All file operations have been done."
    else:
        print "FAILED. Some file operation failed."
        print "The test data has been recovered to its original state."

def output_status_on_checking_failed(num_test_cases):
    print ""
    print "Number of test case(s): {}.".format(num_test_cases)
    print "FAILED. Some test failed."
    print "No file operations have been performed."
    print "The original test data is not modified."

def output_when_no_test_cases_found(is_simple=False):
    if is_simple:
        return
    print "No test cases have been found."
    print "There is nothing to be done."
