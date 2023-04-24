#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ulalib.pathutils as ptu
from ulalib.ula_setting import *

__date__ = "17-04-2023"
__version__ = "0.1.1"
__author__ = "Marta Materni"


def make_dir(path_str, mode=0o777):
    path = ptu.abs(path_str)
    ptu.make_dir(path, mode)
    print(path)


def make_dirs():
    try:
        make_dir(ULA_DATA_DIR)

        make_dir(TEXT_DIR)
        make_dir(TEXT_BACK_DIR)
        make_dir(TEXT_SRC_DIR)

        make_dir(DATA_DIR)
        make_dir(DATA_BACK_DIR)

        make_dir(CORPUS_DIR)
        make_dir(CORPUS_BACK_DIR)

        make_dir(DATA_EXPORT_DIR)

        make_dir(TMP_DIR)
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    make_dirs()
