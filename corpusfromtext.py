#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from ulalib.update_data import UpdateData
from ulalib.ula_setting import CORPUS_NAME
from ulalib.save_back import save_corpus_data_back

__date__ = "30-03-2022"
__version__ = "0.1.4"
__author__ = "Marta Materni"

"""
Aggiorna data_corpus/corpus.form.csv
con i dati di data/text_name.form.csv
"""


def do_main(text_path):
    text_name = os.path.basename(text_path)
    print(text_name)
    save_corpus_data_back(CORPUS_NAME)
    upd_data = UpdateData()
    upd_data.set_text_name(text_name)
    upd_data.update_corpus_forms()


if __name__ == "__main__":
    le = len(sys.argv)
    if le < 2:
        print(f"\nauthor: {__author__}")
        print(f"release: {__version__} { __date__}")
        h = """ 
corpusfromtext.py <name.form.csv> 
        """
        print(h)
        sys.exit()
    text_path = sys.argv[1]
    do_main(text_path)
