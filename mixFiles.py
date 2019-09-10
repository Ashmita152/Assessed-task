#!/usr/bin/python3

import os
import sys
import logging
import argparse
import traceback

NEWLINE = "\n"
DELIMITER = "=========="
FINALFILE = "composite.txt"

def file_to_arr(file):
    try:
        with open(file, 'r') as fd:
            txt = fd.read()
            return txt.split(DELIMITER)
    except Exception:
        logging.error(traceback.format_exc())

def arr_to_file(kw1, kw2, file):
    len_kw1 = len(kw1)
    len_kw2 = len(kw2)
    len_fin = min(len_kw1, len_kw2)

    try:
        with open(file, 'w') as fd:
            fd.write(DELIMITER + NEWLINE)
            for idx in range(len_fin):
                fd.write(kw1[idx])
                fd.write(DELIMITER + NEWLINE)
                fd.write(kw2[idx])
                fd.write(DELIMITER + NEWLINE)
    except Exception:
        logging.error(traceback.format_exc())

def main():
    parser = argparse.ArgumentParser(description='File Mixer')
    parser.add_argument(
        '--keyword1', 
        dest='keyword1',
        type=str,
        default='cricket',
        help='First keyword i.e first filename prefix'
    )
    parser.add_argument(
        '--keyword2', 
        dest='keyword2',
        type=str,
        default='football',
        help='Second keyword i.e second filename prefix'
    )
    args = parser.parse_args()

    kw1 = file_to_arr(args.keyword1 + ".txt")
    kw2 = file_to_arr(args.keyword2 + ".txt")

    arr_to_file(kw1, kw2, FINALFILE)

if __name__ == '__main__':
    sys.exit(main())