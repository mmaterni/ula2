#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from ulalib.update_data import UpdateData
from ulalib.ula_setting import CORPUS_NAME
import os

__date__ = "09-04-2022"
__version__ = "0.1.4"
__author__ = "Marta Materni"

"""Aggiorna data/text_name.form.csv
 con i dati di data_corpus/corpus.form.csv
"""

def do_main(text_path):
    text_name = os.path.basename(text_path)
    print(text_name)
    upd = UpdateData()
    upd.set_text_name(text_name)
    upd.update_text_forms()


if __name__ == "__main__":
    le = len(sys.argv)
    if le < 2:
        print(f"\nauthor: {__author__}")
        print(f"release: {__version__} { __date__}")
        h = """ 
corpusttotext.py <name.form.csv>
        """
        print(h)
        sys.exit()
    text_path = sys.argv[1]
    do_main(text_path)
