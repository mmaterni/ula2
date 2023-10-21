#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# import argparse
import pathlib as pth
import shutil
import os
from ulalib.ula_setting import *

__date__ = "06-05-2022"
__version__ = "0.2.1"
__author__ = "Marta Materni"


def get_token_tmp_path(text_name, ext=""):
    token_name = text_name.replace(".txt", f".token{ext}.csv")
    token_tmp_path = os.path.join(TMP_DIR, token_name)
    return token_tmp_path

def get_token_path(text_name):
    token_name = text_name.replace(".txt", f".token.csv")
    token_path = os.path.join(DATA_DIR, token_name)
    return token_path


def move_path(path1, path2):
    pth.Path(path2).unlink(missing_ok=True);
    shutil.move(path1, path2)

def readd_text_upd(text_path):
    text_name = os.path.basename(text_path)
    "text/name.txt => data/name.token.csv"
    tk_path = get_token_path(text_name)
    tk_path1 = get_token_tmp_path(text_name, "1")
    fr_path = tk_path.replace(".token", ".form")
    fr_path1 = tk_path1.replace(".token", ".form")

    # if ptu.exists(token_path1) is False:
    if pth.Path(tk_path1).exists() is False:
        print(f"{tk_path1} Non  esistente")
        sys.exit()

    print(text_path)
    print(text_name)
    print(tk_path)
    print(tk_path1)
    print(fr_path1)
    print(fr_path)

    # tmp/name.token1.cv => data/name.token.csv
    # tmp/name.form1.cv => data/name.form.csv
    move_path(tk_path1, tk_path)
    move_path(fr_path1, fr_path)


def do_main(text_path):
    readd_text_upd(text_path)

if __name__ == "__main__":
    le = len(sys.argv)
    if le < 2:
        print(f"\nauthor: {__author__}")
        print(f"release: {__version__} { __date__}")
        h=""" 

textunpd.py <text_path>
        """
        print(h)
        sys.exit()
    text_path = sys.argv[1]
    do_main(text_path)



# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     if len(sys.argv) == 1:
#         print(f"\nauthor: {__author__}")
#         print(f"release: {__version__} { __date__}")
#         parser.print_help()
#         sys.exit()
#     parser.add_argument(
#         '-i',
#         dest="src",
#         required=True,
#         metavar="",
#         help="-i <text_path>")
#     args = parser.parse_args()
#     do_main(args.src)
