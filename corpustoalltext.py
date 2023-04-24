#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from ulalib.update_data import UpdateData
from ulalib.ula_setting import *

__date__ = "09-04-2022"
__version__ = "0.1.0"
__author__ = "Marta Materni"


def update_all_text():
    """
    aggiorna tutti i
    data/*.form.csv
    utilizzando:
    data/text_lsit.txt
    data_corpus/corpus.form.csv
    """
    try:
        upd_data=UpdateData()
        upd_data.update_all_text_forms()
    except Exception as e:
        msg = f'ERROR upd_all_text \n{e}'
        sys.exit(msg)


if __name__ == "__main__":
   update_all_text()