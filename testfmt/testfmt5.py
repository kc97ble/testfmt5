#!/usr/bin/env python3

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
import functools

import misc
import format
import filelist
import formatpair

from filelist import BaseFileList, FileList, ZipFileList

def best_format_pair(files):
    return max(
        formatpair.ALL_KNOWN_FORMAT_PAIRS,
        key = lambda pair: len(get_ifiles_ofiles(files, pair.ifmt, pair.ofmt)[0])
    )

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


def do_detect(file_list, sifmt, sofmt, simple=False, **kwargs):
    """ (FileList, Format, Format, ...) -> None
    Outputs input and output file list with the given formats. """
    
    assert (sifmt is None) == (sofmt is None)
    if sifmt is None and sofmt is None:
        pair = best_format_pair(file_list.files)
        sifmt, sofmt = pair.ifmt, pair.ofmt
        assert sifmt is not None
        assert sofmt is not None
    
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

def do_convert(file_list, sifmt, sofmt, difmt, dofmt, preview=False, simple=False, **kwargs):
    """ (FileList|ZipFileList, Format, Format, Format, Format, ...) -> None)
    Moves files in preview mode or real mode. """
    
    assert (sifmt is None) == (sofmt is None)
    if sifmt is None and sofmt is None:
        pair = best_format_pair(file_list.files)
        sifmt, sofmt = pair.ifmt, pair.ofmt
        assert sifmt is not None
        assert sofmt is not None
        
    assert (difmt is None) == (dofmt is None)
    if difmt is None and dofmt is None:
        difmt, dofmt = formatpair.DEFAULT_IFMT, formatpair.DEFAULT_OFMT

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

def get_file_list(path, alphabet, **kwargs):
    assert path != ''
    if zipfile.is_zipfile(path):
        os.chdir(os.path.dirname(path) or '.')
        file_list = ZipFileList(os.path.basename(path))
    else:
        os.chdir(path)
        file_list = FileList.from_working_directory()
    
    if alphabet:
        file_list.files.sort(key=functools.cmp_to_key(misc.cmp_general))
    else:
        file_list.files.sort(key=functools.cmp_to_key(misc.cmp_human))
    
    return file_list

def handle_list(args):
    file_list = get_file_list(**vars(args))
    print('\n'.join(file_list.files))
    
def handle_detect(args):
    file_list = get_file_list(**vars(args))
    #ifiles, ofiles = get_ifiles_ofiles(file_list.files, args.sifmt, args.sofmt)
    #misc.output_detect_result(ifiles, ofiles, args.simple)
    do_detect(file_list, **vars(args))

def handle_convert(args):
    file_list = get_file_list(**vars(args))
    do_convert(file_list, **vars(args))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('path')
    parser_list.add_argument('-a', '--alphabet', action='store_true', help="Sort alphabetically")
    parser_list.set_defaults(handle=handle_list)
    
    parser_detect = subparsers.add_parser('detect')
    parser_detect.add_argument('path')
    parser_detect.add_argument('--sifmt', type=format.Format.from_string)
    parser_detect.add_argument('--sofmt', type=format.Format.from_string)
    parser_detect.add_argument('-a', '--alphabet', action='store_true', help="Sort alphabetically")
    parser_detect.add_argument('-s', '--simple', action='store_true', help="Use simple output format")
    parser_detect.set_defaults(handle=handle_detect)
    
    parser_convert = subparsers.add_parser('convert')
    parser_convert.add_argument('path')
    parser_convert.add_argument('--sifmt', type=format.Format.from_string)
    parser_convert.add_argument('--sofmt', type=format.Format.from_string)
    parser_convert.add_argument('--difmt', type=format.Format.from_string)
    parser_convert.add_argument('--dofmt', type=format.Format.from_string)
    parser_convert.add_argument('-a', '--alphabet', action='store_true', help="Sort alphabetically")
    parser_convert.add_argument('-s', '--simple', action='store_true', help="Use simple output format")
    parser_convert.add_argument('-p', '--preview', action='store_true')
    parser_convert.set_defaults(handle=handle_convert)

    args = parser.parse_args()
    args.handle(args)
