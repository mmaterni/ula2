#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from pdb import set_trace
# from ulalib.ualog import Log
import sys
import argparse
# import ulalib.pathutils as ptu
import os
from ulalib.ula_setting import *
import csv
import pandas as pd

__date__ = "21-05-2023"
__version__ = "0.2.0"
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

POS_MSD_CSV_PATH = "static/cfg/pos_msd.csv"

# path_err = "log/exportdata.ERR.log"
# logerr = Log("w").open(path_err, 1).log
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

    def __init__(self, exp_name):
        self.exp_name = exp_name
        self.pos_msd_json = {}
        #lista di msd_name nel corpus
        self.corpus_msd_lst = []
        self.corpus_msd_blks = []
        # lista delle sigle nel corpus
        self.corpus_sg_lst = []
        self.sigla = 'x'

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
        # TODO check attrs
        # self.check_attrs()
        self.corpus_msd_lst = list(msd_set)
        self.corpus_msd_lst.sort()
        #list msd vuote
        self.corpus_msd_blks = ['' for i in range(len(self.corpus_msd_lst))]

    #estrae dalla lista di tutto il corpus il
    #set di sigle utilizzato
    def get_corpus_sigle(self, rows):
        st = set()
        for row in rows:
            sg = set(row[SIGLA].split(','))
            st.update(sg)
        st.remove('')
        sg_lst = list(st)
        sg_lst.sort()
        #lista sigle di tutto il corpus
        self.corpus_sg_lst = sg_lst

    #controlla attributi dulicati per pos
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
                pass
                # print("|".join(atrr_lst))
                # input('')

    def export_corpus(self):

        # aggiunge le sigle ordinate alla row e inserisce attrs
        def build_row(row):
            #sigle della riga
            sgs = row[SIGLA].split(',')
            sgs = [x for x in sgs if x != '']
            #distribuisce le sigle di riga nella lista delle sigle del corpus
            row_sgs = [x if x in sgs else '' for x in self.corpus_sg_lst]

            #attributi di riga escluso '' e minuscoli
            row_attrs = row[MSD].split(',')
            row_attrs = [x for x in row_attrs if x != '']
            row_attrs = [x.lower() for x in row_attrs]
            pos = row[POS].lower()
            if pos == '':
                # print(row)
                return None
            pos_js = self.pos_msd_json[pos]
            msd_list = pos_js['msd_list']
            # contenitore per distribuire msd sulla riag in funzione di attr
            row_msd_lst = self.corpus_msd_blks.copy()

            #attrs della riga distribuiti sulle colonne dei nomi msd del corpus
            for i, attr in enumerate(row_attrs):
                #lista mse del pos
                for js in msd_list:
                    msd_name = js['msd_name']
                    msd_attrs = js['attrs']
                    #atttributo di riga appartien agli atattrs  del msd corrente
                    if attr in msd_attrs:
                        #TODO controllo attr duplicati
                        #gestione attr duplicati in lista per pos
                        if attr == 'ind' and i == 1:
                            continue
                        if attr == 'imp' and i == 2:
                            continue
                        #setta nella lista attrs da esportare l'attr di riga
                        #alla posizione del nome msd corrispondente
                        idx = self.corpus_msd_lst.index(msd_name)
                        row_msd_lst[idx] = attr
                        break
                # if attr in ['imp','ind']:
                #     print(msd_name, attr, i, ",".join(row_attrs))
            #assegnazione pos_name
            pos_name = self.pos_msd_json[pos]['pos_name']
            row[POS] = pos_name
            row_exp = row[:MSD] + row_msd_lst + row_sgs
            del row_exp[FORMAKEY]
            return row_exp

        corpus_path = os.path.join(CORPUS_DIR, CORPUS_NAME)
        rows = []
        try:
            f = open(corpus_path, 'r', encoding=ENCODING)
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                rows.append(row)
            f.close()
        except Exception as e:
            sys.exit(e)
        exp_name = f"corpus.{self.exp_name}.csv"
        exp_path = os.path.join(DATA_EXPORT_DIR, exp_name)
        print(os.linesep)
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
        token_name = text_name.replace(".txt", ".token.csv")
        token_path = os.path.join(DATA_DIR, token_name)
        form_name = text_name.replace(".txt", ".form.csv")
        form_path = os.path.join(DATA_DIR, form_name)
        # tab12_name = text_name.replace(".txt", ".ula.csv")
        tab12_name = text_name.replace(".txt", f".{self.exp_name}.csv")
        tab12_path = os.path.join(DATA_EXPORT_DIR, tab12_name)
        print(tab12_path)

        tab1 = pd.read_csv(token_path, delimiter='|', header=None)
        tab2 = pd.read_csv(form_path, delimiter='|', header=None)
        formakey = tab2[1].duplicated().any()
        if formakey:
            print("La chiave formaskey non è unica.")
        tab1 = tab1.rename(columns={1: 'col2'})
        tab2 = tab2.rename(columns={1: 'col2'})
        tab12 = pd.merge(tab1, tab2, on='col2', how='left')
        tab12 = tab12.drop(tab12.columns[[1, 2]], axis=1)
        tab12[''] = self.sigla
        tab12 = tab12.fillna('')
        tab12.iloc[:, 6] = tab12.iloc[:, 6].str.lower()

        head = ["FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT", "MSD", "SG"]
        tab12.to_csv(tab12_path, sep='|', header=head, index=False)

    def read_text_list(self):
        try:
            with open(TEXT_LIST_PATH, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
        except Exception as e:
            msg = f'ERROR read_text_lst \n{e}\n'
            sys.exit(msg)
        names = [x.strip() for x in lst]
        return names

    def export_data(self):
        # path = ptu.abs(DATA_EXPORT_DIR)
        # path = os.path.abspath(DATA_EXPORT_DIR)
        # ptu.make_dir(path, 0o777)
        names = self.read_text_list()
        for name in names:
            if name.strip() == '':
                continue
            self.sigla = name.split('.')[-1:][0]
            text_name = name + ".txt"
            self.export_token_form(text_name)
        self.export_corpus()


def do_main(corpus_export_name):
    exportdata = ExportData(corpus_export_name)
    exportdata.export_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    print(f"\nauthor: {__author__}")
    print(f"release: {__version__} { __date__}\n")
    parser.add_argument('-n',
                        dest="name",
                        required=False,
                        default="ula",
                        metavar="",
                        help="-n <corpus_name> (default ula)")
    args = parser.parse_args()
    do_main(args.name)
