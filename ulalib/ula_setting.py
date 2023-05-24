#!/usr/bin/env python
# -*- coding: utf-8 -*-


ULA_DATA_DIR="ula_data"

DATA_DIR = f"{ULA_DATA_DIR}/data"
DATA_BACK_DIR = f"{ULA_DATA_DIR}/data_back"

TEXT_DIR = f"{ULA_DATA_DIR}/text"
TEXT_BACK_DIR = f"{ULA_DATA_DIR}/text_back"
TEXT_SRC_DIR = f"{ULA_DATA_DIR}/text_src"
TEXT_LIST_PATH = f'{ULA_DATA_DIR}/data/text_list.txt'

CORPUS_NAME = f"corpus.form.csv"
CORPUS_DIR = f"{ULA_DATA_DIR}/data_corpus"
CORPUS_BACK_DIR = f"{ULA_DATA_DIR}/data_corpus_back"

DATA_EXPORT_DIR = f"{ULA_DATA_DIR}/data_export"
EXP_LOC_DAT_PATH = f"{DATA_EXPORT_DIR}/exp_loc_dat.csv"

TMP_DIR = f"{ULA_DATA_DIR}/tmp"

POS_MSD_CSV_PATH = "static/cfg/pos_msd.csv"

# ENCODING = 'ISO-8859-1'
ENCODING = 'utf-8'
# PUNCTS = ',.;::?!^~()[]{}<>=+*#@£&%/\\«»“"\'-`‘’'
# APOSTROFO, TRATTINO, PUNTINO gestiti con i token
# NOPUNTS="’-·"
PUNCTS = ',.;::?!^~()[]{}<>=+*#@£&%/\\«»“"\'`‘'

# attacca a
# sinistra# l’altra => l’ altra
# destra#   de·l destrucion => de ·l destrucion
#           destruci-on => destruci -on
BL = ' '
PTR_CHS = [r"\s*[’]\s*",
           r"\s*[-]\s*",
           r"\s*[·]\s*"]
CHS_LR = ['’'+BL,
          BL+'-',
          BL+'·']
