#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from pdb import set_trace
# from ulalib.ualog import Log
import ulalib.pathutils as ptu
import sys
import argparse
import os
import pandas as pd

ULA_DATA_DIR = "ula_data"
DATA_DIR = f"{ULA_DATA_DIR}/data"
# DATA_BACK_DIR = f"{ULA_DATA_DIR}/data_back"
# TEXT_DIR = f"{ULA_DATA_DIR}/text"
# TEXT_BACK_DIR = f"{ULA_DATA_DIR}/text_back"
# TEXT_SRC_DIR = f"{ULA_DATA_DIR}/text_src"
TEXT_LIST_PATH = f'{ULA_DATA_DIR}/data/text_list.txt'
# CORPUS_NAME = f"corpus.form.csv"
# CORPUS_DIR = f"{ULA_DATA_DIR}/data_corpus"
# CORPUS_BACK_DIR = f"{ULA_DATA_DIR}/data_corpus_back"
DATA_EXPORT_DIR = f"{ULA_DATA_DIR}/data_restored"
# EXP_LOC_DAT_PATH = f"static/cfg/exp_loc_dat.csv"
# TMP_DIR = f"{ULA_DATA_DIR}/tmp"
# POS_MSD_CSV_PATH = "static/cfg/pos_msd.csv"
ENCODING = 'utf-8'
# PUNCTS = ',.;::?!^~()[]{}<>=+*#@£&%/\\«»“"\'`‘'
# BL = ' '
# PTR_CHS = [r"\s*[’]\s*", r"\s*[-]\s*", r"\s*[·]\s*"]
# CHS_LR = ['’' + BL, BL + '-', BL + '·']







class RestoreData(object):

    def __init__(self):
        pass

    def restore_token(self, text_path):
        text_name = os.path.basename(text_path)
        token_name = f"{text_name}.token.csv"
        token_path = os.path.join(DATA_DIR, token_name)
        exp_path = os.path.join(DATA_EXPORT_DIR, token_name)
        print(exp_path)
        df = pd.read_csv(token_path, sep='|', header=None)
        df[1] = df[0]
        df.to_csv(exp_path, sep='|', header=False, index=False)

    """
    li|li||||||
    li|li|||fr.m.,XIII||auxMod|
    a|a|avoir|HABERE||VERB||Fin,Ind,Pres,Act,Trans,3,Sing
    """

    def restore_form(self, text_path):
        text_name = os.path.basename(text_path)
        token_name = f"{text_name}.form.csv"
        form_path = os.path.join(DATA_DIR, token_name)
        exp_path = os.path.join(DATA_EXPORT_DIR, token_name)
        print(exp_path)
        df = pd.read_csv(form_path, sep='|', header=None)
        ######
        df = df[~df[1].str.endswith(tuple(map(str, range(10))))]
        mask = df.iloc[:, 0] == df.iloc[:, 1]
        df1 = df[mask]
        df1.iloc[:, 2:] = ''
        ######
        # arr0 = df.values
        # arr1 = [x for x in arr0 if x[0] == x[1]]
        # df = pd.DataFrame(arr1)
        df1.to_csv(exp_path, sep='|', header=False, index=False)

    def read_text_list(self):
        try:
            with open(TEXT_LIST_PATH, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
        except Exception as e:
            msg = f'ERROR read_text_lst \n{e}\n'
            sys.exit(msg)
        names = [x.strip() for x in lst]
        return names

    def make_dir(self,path_str, mode=0o777):
        path = ptu.abs(path_str)
        ptu.make_dir(path, mode)
        print(path)

    def restore_data(self):
        self.make_dir(DATA_EXPORT_DIR)
        names = self.read_text_list()
        for name in names:
            if name.strip() == '':
                continue
            self.restore_token(name)
            self.restore_form(name)


def do_main():
    rd = RestoreData()
    rd.restore_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    do_main()
