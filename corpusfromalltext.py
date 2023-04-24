#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from ulalib.update_data import UpdateData
from ulalib.save_back import save_corpus_data_back
from ulalib.ualog import Log
from ulalib.update_data import UpdateData
from ulalib.ula_setting import *
import ulalib.pathutils as ptu

__date__ = "05-05-2022"
__version__ = "0.0.1"
__author__ = "Marta Materni"

"""
Aggiorna data_corpus/corpus.form.csv
con i dati di tutti i testi

"""


def read_text_list():
    try:
        with open(TEXT_LIST_PATH, 'r', encoding=ENCODING) as f:
            lst = f.readlines()
    except Exception as e:
        msg = f'ERROR read_text_lst \n{e}\n'
        sys.exit(msg)
    names = [x.strip()+".txt" for x in lst]
    return names


def all_text_update_corpus():
    save_corpus_data_back(CORPUS_NAME)
    text_lst = read_text_list()
    try:
        for text_name in text_lst:
            print(text_name)
            upd_data = UpdateData()
            upd_data.set_text_name(text_name)
            upd_data.update_corpus_forms()
    except Exception as e:
        msg = f'ERROR upd_corpus_all \n{e}'
        sys.exit(msg)


if __name__ == "__main__":
    all_text_update_corpus()
