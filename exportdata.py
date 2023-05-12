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

POS_MSD_JS_PATH = "static/cfg/pos_msd.json"

path_err = "log/exportdata.ERR.log"
logerr = Log("w").open(path_err, 1).log


class ExportData(object):

    def __init__(self, corpus_exp_name, csv_sep='\t'):
        self.corpus_exp_name = corpus_exp_name
        self.sep = csv_sep

        self.msd_attr_lst = []
        self.msd_attr_head = []
        self.msd_blk_lst = []
        self.msd_attr_idx = {}

        self.sigle_head = []
        self.sigle_js = {}
        self.sigle_blk_lst = []

    def read_pos_msd(self):
        if pth.Path(POS_MSD_JS_PATH).exists() is False:
            msg = "pos_msd.jsson Not Found."
            logerr(msg)
            sys.exit()
        try:
            with open(POS_MSD_JS_PATH, 'r', encoding=ENCODING) as f:
                s = f.read()
                s = s.lower()
                pos_msd_js = json.loads(s)
        except Exception as e:
            msg = f'ERROR read_pos_msd_js \n{e}\n'
            raise Exception(msg)

        #lista msd name
        msd_set = set()
        #dict k=pos_attr v=msd_name
        pos_attr_js = {}
        for kv in pos_msd_js.items():
            p_k = kv[0]
            p_js = kv[1]
            m_lst = p_js['msd_list']
            for m_js in m_lst:
                m_name = m_js['msd_name']
                msd_set.add(m_name)
                attrs = m_js['attrs']
                for a in attrs:
                    p_a_k = f'{p_k}_{a}'
                    pos_attr_js[p_a_k] = m_name
        #elimina duplicati
        self.msd_attr_lst = list(msd_set)
        self.msd_attr_lst.sort()
        self.msd_attr_head = [x.upper() for x in self.msd_attr_lst]
        #list msd vuote
        self.msd_blk_lst = ['' for i in range(len(self.msd_attr_lst))]

        #dict k=pos_attr v=idx
        #idx indice di m_name in msd_head
        pos_attr_idx_js = {}
        for kv in pos_attr_js.items():
            k = kv[0]
            m_name = kv[1]
            idx = self.msd_attr_lst.index(m_name)
            pos_attr_idx_js[k] = idx
        self.msd_attr_idx = pos_attr_idx_js

    #estrae dalla lista di tutto il corpus il
    #set di sigle utilizzato
    def get_corpus_sigle(self, rows):
        st = set()
        for row in rows:
            cols = row.strip().split('|')
            sg = set(cols[SIGLA].split(','))
            st.update(sg)
        st.remove('')
        sg_lst = list(st)
        sg_lst.sort()
        #lista sigle di tutto il corpus
        self.sigle_head = sg_lst
        #dictionario delle sigle del corpus
        self.sigle_js = {x: i for i, x in enumerate(sg_lst)}
        #list di sigle vuote
        self.sigle_blk_lst = ['' for i in range(len(sg_lst))]

    def export_corpus(self):

        # aggiunge le sigle ordinate alla row
        def build_row(row):
            print(row)
            r = row.split('|')

            #sigle della riga
            r_sg_lst = r[SIGLA].split(',')
            r_sg_lst = [x for x in r_sg_lst if x != '']
            #sigle ordinate per la riga
            row_sg_lst = self.sigle_blk_lst.copy()
            for s in r_sg_lst:
                i = self.sigle_js[s]
                row_sg_lst[i] = s

            #attrs della riga
            r_attr_lst = r[MSD].split(',')
            r_attr_lst = [x.lower() for x in r_attr_lst]
            r_attr_lst = [x for x in r_attr_lst if x != '']
            #sigle ordinate per la riga
            row_attr_lst = self.msd_blk_lst.copy()
            pos = r[POS].lower()
            for attr in r_attr_lst:
                k = f'{pos}_{attr}'
                idx = self.msd_attr_idx[k]
                row_attr_lst[idx] = attr

            row = r[:FUNCT] + row_attr_lst
            #elimina le sigle originarie e aggiuge la lista delle sigke
            row = row[:-1]
            row.extend(row_sg_lst)
            #elimina formakey
            del row[1]
            return row

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

            # #lista sigle di tutto il corpus
            self.get_corpus_sigle(rows)
            #dict di pos_attr e lista msd nme  pos_msd.json
            self.read_pos_msd()

            #AAA intestazione comprensiva delle sigle e msd
            head_corpus = ["FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT"]
            # head = head_corpus + msd_lst + sg_lst
            head = head_corpus + self.msd_attr_head + self.sigle_head

            row = self.sep.join(head)
            fw.write(row)
            fw.write(os.linesep)

            rows.sort()
            for item in rows:
                item = item.strip()
                #aggiunge set msd attr e aggiunge le sigle alla row
                r = build_row(item)
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
