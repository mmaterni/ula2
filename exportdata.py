#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import sys
import argparse
import pathlib as pth
import os
from ulalib.ula_setting import *
# from openpyxl import Workbook

__date__ = "02-01-2023"
__version__ = "0.1.1"
__author__ = "Marta Materni"

#form.csv
# abandonés|abandonés|abandoner|*BAN||VERB|compPass|Ind,Part,Past,Sing,Masc,MWEs
FORMA = 0
FORMAKEY = 1
LEMMA = 2
ETIMO = 3
LANG = 4
POS = 5
FUNCT = 6
MSD = 7
TOKEN_ROW_LEN = 8

#token.csv
#coment|coment
#FORMA = 0
#FORMAKEY = 1
TOKEN_ROW_LEN = 2

#HEAD = ["FORMA", "FORMAKEY", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT", "MSD"]
HEAD = ["FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT", "MSD"]


class ExportData(object):

    def __init__(self, dir_exp, csv_sep='\t'):
        self.dir_exp = dir_exp
        self.sep = csv_sep

    def export_corpus(self):
        corpus_path = os.path.join(CORPUS_DIR, CORPUS_NAME)
        if pth.Path(corpus_path).exists() is False:
            print(f"{corpus_path} Non  esistente")
            sys.exit()
        lst = []
        try:
            with open(corpus_path, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
        except Exception as e:
            msg = f'ERROR export_corpus \n{e}\n'
            print(msg)
            raise Exception(msg)
        try:
            # head_csv = self.sep.join(HEAD)
            corpus_name = CORPUS_NAME.replace('csv', '.ula.csv')
            exp_path = os.path.join(self.dir_exp, corpus_name)
            print(exp_path)
            fw = open(exp_path, "w", encoding=ENCODING)
            lst.sort()
            for item in lst:
                item0=[]
                r=item.split('|')
                for i,x in enumerate(r):
                    if i==1:
                        continue
                    item0.append(x)
                row=self.sep.join(item0)
                # row = item0.replace('|', self.sep)
                fw.write(row)
                # fw.write(os.linesep)
            fw.close()
            os.chmod(exp_path, 0o777)
        except IOError as e:
            msg = f'ERROR export_corpus: \n{e}\n'
            raise Exception(msg)

    def read_form_csv(self, text_name):
        form_name = text_name.replace(".txt", f".form.csv")
        form_path = os.path.join(DATA_DIR, form_name)
        if pth.Path(form_path).exists() is False:
            print(f"{form_path} Non  esistente")
            sys.exit()
        form_lst = []
        form_keys = []
        try:
            with open(form_path, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
            for i, row in enumerate(lst):
                row = row.strip()
                if row == "":
                    break
                cols = row.split('|')
                if len(cols) < TOKEN_ROW_LEN:
                    self.logerr(f"text\n{i}\n{row}\n{cols}\n")
                    continue
                form_lst.append(cols)
                key = cols[FORMAKEY]
                form_keys.append(key)
            return form_lst, form_keys
        except Exception as e:
            msg = f'ERROR read_form_csv \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)

    def read_token_csv(self, text_name):
        token_name = text_name.replace(".txt", f".token.csv")
        token_path = os.path.join(DATA_DIR, token_name)
        if pth.Path(token_path).exists() is False:
            print(f"{token_path} Non  esistente")
            sys.exit()
        token_lst = []
        try:
            with open(token_path, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
            for i, row in enumerate(lst):
                row = row.strip()
                if row == "":
                    break
                cols = row.split('|')
                if len(cols) < TOKEN_ROW_LEN:
                    self.logerr(f"text\n{i}\n{row}\n{cols}\n")
                    continue
                token_lst.append(cols)
            return token_lst
        except Exception as e:
            msg = f'ERROR read_token_csv \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)

    def join_token_form(self, token_lst, form_lst, form_keys):
        form_empty = ["", "", "", "", "", "", "", ""]
        token_form_lst = []
        for token in token_lst:
            key = token[FORMAKEY]
            try:
                idx = form_keys.index(key)
            except ValueError:
                form = form_empty
                form[0] = token[0]
                form[1] = token[1]
            else:
                form = form_lst[idx]
            token_form_lst.append(form)
        return token_form_lst

    def write_token_form_csv(self, exp_path, token_fom_lst):
        try:
            head_csv = self.sep.join(HEAD)
            fw = open(exp_path, "w", encoding=ENCODING)
            fw.write(head_csv)
            fw.write(os.linesep)
            for item in token_fom_lst:
                
                item0 = []
                for i, x in enumerate(item):
                    if i == 1:
                        continue
                    item0.append(x)
                row = self.sep.join(item0)

                fw.write(row)
                fw.write(os.linesep)
            fw.close()
            os.chmod(exp_path, 0o777)
        except IOError as e:
            msg = f'ERROR write_token_form_csv: \n{e}\n'
            sys.exit(msg)

    def export_text_data(self, text_path):
        text_name = os.path.basename(text_path)
        token_lst = self.read_token_csv(text_name)
        form_lst, form_keys = self.read_form_csv(text_name)
        token_form_lst = self.join_token_form(token_lst, form_lst, form_keys)
        exp_name = text_name.replace(".txt", ".ula.csv")
        exp_csv_path = os.path.join(self.dir_exp, exp_name)
        print(exp_csv_path)
        self.write_token_form_csv(exp_csv_path, token_form_lst)

    def read_text_list(self):
        if pth.Path(TEXT_LIST_PATH).exists() is False:
            msg = "text_list.txt Not Found."
            print(msg)
            sys.exit()
        try:
            with open(TEXT_LIST_PATH, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
        except Exception as e:
            msg = f'ERROR read_text_lst \n{e}\n'
            raise Exception(msg)
        names = [x.strip() for x in lst]
        return names

    def export_data(self):
        path = pth.Path(self.dir_exp)
        path.mkdir(exist_ok=True)
        os.chmod(self.dir_exp, 0o777)
        names = self.read_text_list()
        for name in names:
            if name.strip() == '':
                continue
            text_name = name + ".txt"
            # print(text_name)
            self.export_text_data(text_name)
        self.export_corpus()


def do_main(dir_exp, csv_sep):
    exportdata = ExportData(dir_exp, csv_sep)
    exportdata.export_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    print(f"\nauthor: {__author__}")
    print(f"release: {__version__} { __date__}\n")
    parser.add_argument('-s',
                        dest="sep",
                        required=False,
                        default='p',
                        metavar="",
                        help='-s p)pipe s)emi_colon t)tab  (default pipe (|))')
    parser.add_argument('-d',
                        dest="dir",
                        required=False,
                        default="./data_export",
                        metavar="",
                        help="-d <dir_export> (default ./data_export)")
    args = parser.parse_args()
    if args.sep == 't':
        sep = '\t'
    elif args.sep == 'p':
        sep = '|'
    elif args.sep == 's':
        sep = ';'
    else:
        print("options for flag -s are t/p/s")
        sys.exit()
    do_main(args.dir, sep)
