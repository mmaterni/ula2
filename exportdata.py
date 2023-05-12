#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
from ulalib.ualog import Log
import sys
import argparse
import pathlib as pth
import ulalib.pathutils as ptu
import os
from ulalib.ula_setting import *

__date__ = "10-05-2023"
__version__ = "0.1.2"
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

SIGLA = 8

TOKEN_ROW_LEN = 2
FORM_ROW_LEN = 2

MSD_CSV_PATH = "static/cfg/msd.csv"

path_err = "log/exportdata.ERR.log"
logerr = Log("w").open(path_err, 1).log


class ExportData(object):

    def __init__(self, corpus_exp_name, csv_sep='\t'):
        self.corpus_exp_name = corpus_exp_name
        self.sep = csv_sep

    def read_msd_csv(self):
        if pth.Path(MSD_CSV_PATH).exists() is False:
            msg = "msd.csv Found."
            logerr(msg)
            sys.exit()
        try:
            with open(MSD_CSV_PATH, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
        except Exception as e:
            msg = f'ERROR read_msd_ccsv \n{e}\n'
            raise Exception(msg)
        #id|name|attrs
        # 1|gender|Masc,Fem,Neut
        # 2|number|Sing,Plur
        # 3|case|Nom,Acc
        msd_lst = []
        msd_attr_lst = []
        for row in lst:
            if row[0] == '#':
                continue
            r = row.lower().split('|')
            msd_lst.append(r[1])

        # AAA sort ?
        return msd_lst

    def get_msd_dict(self, lst):
        js = {}
        for i, msd in enumerate(lst):
            attrs = msd.split(',')
            for a in attrs:
                js[a] = i
        return js

    #estrae dalla lista di tutto il corpus il
    #set di sigle utilizzato
    def get_corpus_sigle(self, rows):
        st = set()
        for row in rows:
            cols = row.strip().split('|')
            sg = set(cols[SIGLA].split(','))
            st.update(sg)
        st.remove('')
        lst = list(st)
        lst.sort()
        return lst

    def export_corpus(self):

        # aggiunge le sigle ordinate alla row
        def add_row_sigle(row, js, lst0):
            lst = lst0.copy()
            r = row.split('|')
            rsg = r[SIGLA].split(',')
            rsg = [x for x in rsg if x != '']
            for s in rsg:
                i = js[s]
                lst[i] = s
            r = r[:-1]
            r.extend(lst)
            return r

        corpus_path = ptu.join(CORPUS_DIR, CORPUS_NAME)
        if pth.Path(corpus_path).exists() is False:
            logerr(f"{corpus_path} Non  esistente")
            sys.exit()
        rows = []
        try:
            with open(corpus_path, 'r', encoding=ENCODING) as f:
                rows = f.readlines()
        except Exception as e:
            msg = f'ERROR export_corpus \n{e}\n'
            logerr(msg)
            raise Exception(msg)
        try:
            # head_csv = self.sep.join(HEAD)
            cexport_name = f"corpus.{self.corpus_exp_name}.csv"
            exp_path = ptu.join(DATA_EXPORT_DIR, cexport_name)
            print(os.linesep)
            print(exp_path)
            fw = open(exp_path, "w", encoding=ENCODING)

            #lista sigle di tutto il corpus
            sg_lst = self.get_corpus_sigle(rows)
            #dictionario delle sigle del corpus
            sg_js = {x: i for i, x in enumerate(sorted(sg_lst))}
            #list di sigle vuote
            sg_blk_lst = ['' for i in range(len(sg_lst))]

            #lista estratta da msd.csv
            msd_lst = self.read_msd_csv()
            #lista di msd vuote
            msd_blk_lst = ['' for i in range(len(msd_lst))]

            #AAA intestazione comprensiva delle sigle e msd
            head_corpus = ["FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT"]
            head = head_corpus + msd_lst + sg_lst

            row = self.sep.join(head)
            fw.write(row)
            fw.write(os.linesep)

            rows.sort()
            for item in rows:
                item = item.strip()

                #aggiunge le sigle alla row
                r = add_row_sigle(item, sg_js, sg_blk_lst)
                # AAA inserire msd
                #elimina formakey
                del r[1]

                row = self.sep.join(r)
                fw.write(row)
                fw.write(os.linesep)
            fw.close()
            os.chmod(exp_path, 0o777)
        except IOError as e:
            msg = f'ERROR export_corpus: \n{e}\n'
            raise Exception(msg)

    def export_token_form(self, text_path):
        text_name = os.path.basename(text_path)
        token_lst = self.read_token_csv(text_name)
        form_lst, form_keys = self.read_form_csv(text_name)
        #aggiunge form ai token
        token_form_lst = self.join_token_form(token_lst, form_lst, form_keys)
        exp_name = text_name.replace(".txt", ".ula.csv")
        exp_csv_path = ptu.join(DATA_EXPORT_DIR, exp_name)
        print(exp_csv_path)
        head_token = [
            "FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT", "MSD", "SIGLE"
        ]
        try:
            head_csv = self.sep.join(head_token)
            fw = open(exp_csv_path, "w", encoding=ENCODING)
            fw.write(head_csv)
            fw.write(os.linesep)
            for item in token_form_lst:
                item0 = []
                for i, x in enumerate(item):
                    if i == 1:
                        continue
                    item0.append(x)
                row = self.sep.join(item0)

                fw.write(row)
                fw.write(os.linesep)
            fw.close()
            os.chmod(exp_csv_path, 0o777)
        except IOError as e:
            msg = f'ERROR write_token_form_csv: \n{e}\n'
            sys.exit(msg)

    ########################

    def read_form_csv(self, text_name):
        form_name = text_name.replace(".txt", f".form.csv")
        form_path = ptu.join(DATA_DIR, form_name)

        if pth.Path(form_path).exists() is False:
            logerr(f"{form_path} Non  esistente")
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
                if len(cols) < FORM_ROW_LEN:
                    logerr(f"text\n{i}\n{row}\n{cols}\n")
                    continue
                form_lst.append(cols)
                key = cols[FORMAKEY]
                form_keys.append(key)
            return form_lst, form_keys
        except Exception as e:
            msg = f'ERROR read_form_csv \n{e}\n'
            logerr(msg)
            raise Exception(msg)

    def read_token_csv(self, text_name):
        token_name = text_name.replace(".txt", f".token.csv")
        token_path = ptu.join(DATA_DIR, token_name)
        if pth.Path(token_path).exists() is False:
            logerr(f"{token_path} Non  esistente")
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
                    logerr(f"text\n{i}\n{row}\n{cols}\n")
                    continue
                token_lst.append(cols)
            return token_lst
        except Exception as e:
            msg = f'ERROR read_token_csv \n{e}\n'
            logerr(msg)
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

    def read_text_list(self):
        if pth.Path(TEXT_LIST_PATH).exists() is False:
            msg = "text_list.txt Not Found."
            logerr(msg)
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
        path = ptu.abs(DATA_EXPORT_DIR)
        ptu.make_dir(path, 0o777)
        names = self.read_text_list()
        # for name in names:
        #     if name.strip() == '':
        #         continue
        #     text_name = name + ".txt"
        #     self.export_token_form(text_name)
        self.export_corpus()


def do_main(corpus_export_name, csv_sep):
    exportdata = ExportData(corpus_export_name, csv_sep)
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
    parser.add_argument('-n',
                        dest="name",
                        required=False,
                        default="ula",
                        metavar="",
                        help="-n <corpus_name> (default ula)")
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
    do_main(args.name, sep)
