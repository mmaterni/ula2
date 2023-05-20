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
import json
import csv

__date__ = "20-05-2023"
__version__ = "0.1.4"
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

# POS_MSD_JS_PATH = "static/cfg/pos_msd.json"
POS_MSD_CSV_PATH = "static/cfg/pos_msd.csv"

path_err = "log/exportdata.ERR.log"
logerr = Log("w").open(path_err, 1).log
"""
POS|pos_name|msd_name|attrs
NOUN|noun|gender|Masc,Fem,Neut
NOUN|noun|number|Sing,Plur
NOUN|noun|case|Nom,Acc

{
  "NOUN": {
    "pos_name": "noun",
    "msd_list": [
      {
        "msd_name": "gender",
        "attrs": [
          "Masc",
          "Fem",
          "Neut"
        ]
      },
      {
        "msd_name": "number",
        "attrs": [
          "Sing",
          "Plur"
        ]
      },
      {
        "msd_name": "case",
        "attrs": [
          "Nom",
          "Acc"
        ]
      }
    ]
  },
"""


class ExportData(object):

    def __init__(self, corpus_exp_name, csv_sep='\t'):
        self.corpus_exp_name = corpus_exp_name
        self.sep = csv_sep
        self.pos_msd_json = {}
        #lista di msd_name nel corpus
        self.corpus_msd_lst = []
        self.corpus_msd_blks = []
        # lista delle sigle nel corpus
        self.corpus_sg_lst = []

    def read_pos_msd_csv(self):
        try:
            f = open(POS_MSD_CSV_PATH)
        except Exception as e:
            sys.ecit(e)
        rows = csv.reader(f, delimiter='|')

        self.pos_msd_json = {}
        msd_set = set()
        next(rows)
        for row in rows:
            row = [x.lower() for x in row]
            pos = row[0]
            pos_name = row[1]
            msd_name = row[2]
            msd_set.add(msd_name)
            attrs = row[3].split(",")
            if pos not in self.pos_msd_json:
                self.pos_msd_json[pos] = {"pos_name": pos_name, "msd_list": []}
            self.pos_msd_json[pos]["msd_list"].append({
                "msd_name": msd_name,
                "attrs": attrs
            })

        f.close()
        #############################################
        # AAA check attrs
        self.check_attrs()
        self.corpus_msd_lst = list(msd_set)
        self.corpus_msd_lst.sort()
        #list msd vuote
        self.corpus_msd_blks = ['' for i in range(len(self.corpus_msd_lst))]

    #estrae dalla lista di tutto il corpus il
    #set di sigle utilizzato
    def get_corpus_sigle(self, rows):
        st = set()
        for row in rows:
            # cols = row.strip().split('|')
            # sg = set(cols[SIGLA].split(','))
            sg = set(row[SIGLA].split(','))
            st.update(sg)
        st.remove('')
        sg_lst = list(st)
        sg_lst.sort()
        #lista sigle di tutto il corpus
        self.corpus_sg_lst = sg_lst

    def check_attrs(self):
        for k, v in self.pos_msd_json.items():
            pos = k
            msd_list = v['msd_list']
            atrr_lst = []
            for js in msd_list:
                attrs = js['attrs']
                atrr_lst.extend(attrs)
            atrr_lst.sort()
            attr_set = sorted(list(set(atrr_lst)))
            x = False
            for a in attr_set:
                n = atrr_lst.count(a)
                if n > 1:
                    x = True
                    print(pos, n, a)
            if x:
                print("|".join(atrr_lst))
                # input('')

    def export_corpus(self):

        # aggiunge le sigle ordinate alla row e inserisce attrs
        def build_row(row):
            # r = row.split('|')
            r = row

            #sigle della riga
            sgs = r[SIGLA].split(',')
            sgs = [x for x in sgs if x != '']
            row_sgs = [x if x in sgs else '' for x in self.corpus_sg_lst]

            #attrs della riga
            row_msd_lst = self.corpus_msd_blks.copy()
            row_attrs = r[MSD].split(',')
            row_attrs = [x for x in row_attrs if x != '']
            row_attrs = [x.lower() for x in row_attrs]
            pos = r[POS].lower()
            if pos == '':
                # return row.split('|')
                return None
            pos_js = self.pos_msd_json[pos]
            msd_list = pos_js['msd_list']
            # distrinuisce msd sulla riag in funzione di attr
            row_msd_lst = self.corpus_msd_blks.copy()
            for i, attr in enumerate(row_attrs):
                for js in msd_list:
                    msd_name = js['msd_name']
                    msd_attrs = js['attrs']
                    if attr in msd_attrs:
                        idx = self.corpus_msd_lst.index(msd_name)
                        row_msd_lst[idx] = attr
                        # if attr=='ind':
                        #     print(msd_name,attr,i,",".join(r_attrs))
                        # if attr=='imp':
                        #     print(msd_name,attr,i,",".join(r_attrs))
                        break

            #assegnazione pos_name
            pos_name = self.pos_msd_json[pos]['pos_name']
            r[POS] = pos_name

            rr = r[:MSD] + row_msd_lst + row_sgs
            del rr[FORMAKEY]
            return rr

        corpus_path = ptu.join(CORPUS_DIR, CORPUS_NAME)
        rows = []
        try:
            f = open(corpus_path, 'r', encoding=ENCODING)
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                rows.append(row)
            f.close()
        except Exception as e:
            sys.exit(e)
        cexport_name = f"corpus.{self.corpus_exp_name}.csv"
        exp_path = ptu.join(DATA_EXPORT_DIR, cexport_name)
        print(exp_path)
        #lista sigle di tutto il corpus
        self.get_corpus_sigle(rows)
        #dict di pos_attr e lista msd nme  pos_msd.json
        self.read_pos_msd_csv()
        try:
            fw = open(exp_path, "w", encoding=ENCODING)
            writer = csv.writer(fw, delimiter='|')
            #intestazione comprensiva delle sigle e msd
            head_corpus = ["FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT"]
            attrs_head = [x.upper() for x in self.corpus_msd_lst]
            head = head_corpus + attrs_head + self.corpus_sg_lst
            writer.writerow(head)
            rows.sort()
            for row in rows:
                r = build_row(row)
                if r is None:
                    continue
                writer.writerow(r)
            fw.close()
            os.chmod(exp_path, 0o777)
        except IOError as e:
            msg = f'ERROR export_corpus: \n{e}\n'
            sys.exit(msg)

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
