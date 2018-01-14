#!/usr/bin/env python2

""" testfmt5.py

Usage:
    testfmt5.py apple/ -i '*.in' -o '*.ans' --detect
    testfmt5.py apple/ -i '*.in' -o '*.ans' -I '*.in' -O '*.ok' --preview
    testfmt5.py apple/ -i '*.in' -o '*.ans' -I '*.in' -O '*.ok'
    testfmt5.py apple.zip -i '*.in' -o '*.ans' --detect
    testfmt5.py apple.zip -i '*.in' -o '*.ans' -I '*.in' -O '*.ok' --preview
    testfmt5.py apple.zip -i '*.in' -o '*.ans' -I '*.in' -O '*.ok'
"""

import os
import sys
import zipfile
import argparse

import misc
import format
import filelist

from filelist import BaseFileList, FileList, ZipFileList

def get_ifiles_ofiles(files, ifmt, ofmt):
    """ (list, Format, Format) -> (list, list) """
    assert isinstance(files, list)
    assert isinstance(ifmt, format.Format)
    assert isinstance(ofmt, format.Format)

    #files = sorted(files)
    ifiles, ofiles = [], []

    for x in files:
        if not ifmt.match(x):
            continue
        y = format.convert_format(x, ifmt, ofmt)
        if y not in files:
            continue
        if (x in ifiles) or (x in ofiles):
            continue
        if (y in ifiles) or (y in ofiles):
            continue
        ifiles.append(x)
        ofiles.append(y)
    return (ifiles, ofiles)

def do_detect(file_list, sifmt, sofmt, simple=False):
    """ (FileList, Format, Format, ...) -> None
    Outputs input and output file list with the given formats. """
    
    ifiles, ofiles = get_ifiles_ofiles(file_list.files, sifmt, sofmt)
    misc.output_detect_result(ifiles, ofiles, simple)

def do_convert_preview(file_list, src, dst, simple=False):
    """ (BaseFileList, list, list, ...) -> None
    Moves files in preview mode. Exits 0 if success or 1 otherwise. """
    
    num_test_cases = misc.ensure_equal_len(src, dst) / 2
    misc.output_src_and_dst(src, dst, simple)
    success = BaseFileList(file_list.files).move_files_indirectly(src, dst, quiet=True)
    misc.output_preview_result(success, num_test_cases, simple)
    sys.exit(0 if success else 1)

def do_convert_execute(file_list, src, dst, simple=False):
    """ (FileList|ZipFileList, list, list, ...) -> None
    Moves files really. Checks first. Exits 0 if success or 1 otherwise. """
    
    num_test_cases = misc.ensure_equal_len(src, dst) / 2
    success = BaseFileList(file_list.files).move_files_indirectly(src, dst, quiet=True)
    if success==False:
        misc.output_status_on_checking_failed(num_test_cases)
        sys.exit(1)
    else:
        success = file_list.move_files_indirectly(src, dst, real=True)
        misc.output_convert_result(success, num_test_cases)
        sys.exit(0 if success else 1)

def do_convert(file_list, sifmt, sofmt, difmt, dofmt, preview=False, simple=False):
    """ (FileList|ZipFileList, Format, Format, Format, Format, ...) -> None)
    Moves files in preview mode or real mode. """

    sifiles, sofiles = get_ifiles_ofiles(file_list.files, sifmt, sofmt)
    difiles = format.convert_format_list(sifiles, sifmt, difmt)
    dofiles = format.convert_format_list(sofiles, sofmt, dofmt)

    src = misc.join_alternatively(sifiles, sofiles)
    dst = misc.join_alternatively(difiles, dofiles)
    num_test_cases = misc.ensure_equal_len(src, dst) / 2

    if num_test_cases == 0:
        misc.output_when_no_test_cases_found(simple)
        sys.exit(0)
    if preview:
        do_convert_preview(file_list, src, dst, simple)
    else:
        do_convert_execute(file_list, src, dst, simple)

if __name__ == '__main__':
    #TODO: make this more friendly
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="Test data directory")
    parser.add_argument('-d', '--detect', action='store_true')
    parser.add_argument('-p', '--preview', action='store_true')
    parser.add_argument('-s', '--simple', action='store_true', help="Use simple output format")
    parser.add_argument('-r', '--reverse', action='store_true', help="Swap sifmt with difmt, sofmt with dofmt")
    parser.add_argument('-i', '--sifmt', type=format.Format)
    parser.add_argument('-o', '--sofmt', type=format.Format)
    parser.add_argument('-I', '--difmt', type=format.Format)
    parser.add_argument('-O', '--dofmt', type=format.Format)
    parser.add_argument('-f', '--infix-fmt', default='', help="Infix format")
    parser.add_argument('-a', '--alphabet', action='store_true', help="Sort alphabetically")
    args = parser.parse_args()

if args.difmt is not None:
    args.difmt.infix_fmt = args.infix_fmt
if args.dofmt is not None:
    args.dofmt.infix_fmt = args.infix_fmt

if args.reverse:
    args.sifmt, args.difmt = args.difmt, args.sifmt
    args.sofmt, args.dofmt = args.dofmt, args.sofmt
    args.reverse = False

if args.simple and not args.preview and not args.detect:
    print >> sys.stderr, "-s is for -d or -p only."

if args.path != '' and zipfile.is_zipfile(args.path):
    os.chdir(os.path.dirname(args.path) or '.')
    file_list = ZipFileList(os.path.basename(args.path))
else:
    os.chdir(args.path or '.')
    file_list = FileList.from_working_directory()

if args.alphabet:
    file_list.files.sort(misc.cmp_general)
else:
    file_list.files.sort(misc.cmp_human)

if args.detect == True:
    assert (args.sifmt is not None) and (args.sofmt is not None)
    do_detect(file_list, args.sifmt, args.sofmt, args.simple)
else:
    assert all(x is not None for x in [args.sifmt, args.sofmt, args.difmt, args.dofmt])
    do_convert(file_list, args.sifmt, args.sofmt, args.difmt, args.dofmt, args.preview, args.simple)
