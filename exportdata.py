#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
# from ulalib.ualog import Log
import sys
import argparse
import os
from ulalib.ula_setting import *
import csv
import pandas as pd

__date__ = "27-05-2023"
__version__ = "0.2.7"
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

# POS_MSD_CSV_PATH = "static/cfg/pos_msd.csv"
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
#tabella decodifica sigle => località,data
"""
g|GRENOBLE|grenoble|XII
h|TOUR|tour|XII
p|PARIS|paris|XIII
v|VENEZIA|venezia|XIV

val_locs=['grenoble','tour','paris','venezia']
head_dats=['XII','XII','XIV']
ljs={
'g':'grenoble',
'h':'tour',
'p':'paris',
'v':'venezia'
}
djs={
'g':[0,'XII'],
'h':[0,'XII'],
'p':[1,'XIII'],
'v':[2,'XIV']
}

"""


class ExportData(object):

    def __init__(self, exp_name):
        self.exp_name = exp_name
        self.pos_msd_json = {}

        #lista di msd_name nel corpus
        self.corpus_msd_lst = []
        self.corpus_msd_blks = []

        # lista delle sigle nel corpus
        self.corpus_sgs = []
        self.text_sigla = 'x'

        #sigle per esportazione
        self.head_locs = []
        self.val_locs = []
        self.head_dates = []
        self.rif_dates = []
        self.exp_sgs = []
        self.locjs = {}
        self.datejs = {}

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
            #TODO controlare maiuscole-minuscole
            # row = [x.lower() for x in row]
            pos = row[0].lower()
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
        # TODO check attrs
        self.check_attrs()
        #elimina msd vuoto
        try:
            msd_set.remove('')
        except KeyError:
            pass
        self.corpus_msd_lst = list(msd_set)
        self.corpus_msd_lst.sort()
        #lista msd vuote
        self.corpus_msd_blks = [''] * len(self.corpus_msd_lst)

    def read_exp_csv(self):
        rows = []
        try:
            with open(EXP_LOC_DAT_PATH, 'r', encoding=ENCODING) as f:
                reader = csv.reader(f, delimiter='|')
                for r in reader:
                    rows.append(r)
        except Exception as e:
            sys.exit(e)
        #set delle date
        DATE = [
            'IX', 'X', 'X1', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII',
            'XVIII', 'XIX', 'XX'
        ]
        ds = {r[3] for r in rows}
        # self.head_dats = [''] * len(ds)
        # label head delle date
        self.head_dates = [f'DATE.{i}' for i in range(len(ds))]
        #date di riferimento per posizionamento date di riga
        self.rif_dates = [x for x in DATE if x in ds]
        for r in rows:
            sg = r[0]
            self.exp_sgs.append(sg)
            self.head_locs.append(r[1])
            self.val_locs.append(r[2])
            self.locjs[sg] = r[2]
            self.datejs[sg] = r[3]

    #estrae dalla lista di tutto il corpus il
    def get_corpus_sigle(self, rows):
        st = set()
        for row in rows:
            sg = row[SIGLA].split(',')
            for x in sg:
                st.add(x)
        try:
            st.remove('')
        except KeyError:
            pass
        sgs = list(st)
        sgs.sort()
        self.corpus_sgs = sgs

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

    #nella riga località e date derivate dalla sigla
    # venezia, ,paris, , XI,..XIV
    def build_row_loc_dat(self, r_sgs):
        #valopri loc di riga
        r_locs = [self.locjs[x] if x in r_sgs else '' for x in self.exp_sgs]
        #valori data di riga
        ds = {self.datejs[x] for x in r_sgs}
        r_dates = [x if x in ds else '' for x in self.rif_dates]
        row = r_locs + r_dates
        return row

    def build_row_msd(self, pos, row_attrs):
        pos_js = self.pos_msd_json[pos]
        pos_msd_list = pos_js['msd_list']
        row_msds = self.corpus_msd_blks.copy()
        print(pos)
        print(row_attrs)
        print(pos_msd_list)
        for i, attr in enumerate(row_attrs):
            print(i, attr)
            #lista mse del pos
            for js in pos_msd_list:
                msd_name = js['msd_name']
                msd_attrs = js['attrs']
                msd_attrs_lower = [x.lower() for x in msd_attrs]
                print("....", msd_name, msd_attrs)
                #atttributo di riga appartien agli atattrs  del msd corrente
                attr_lower = attr.lower()
                if attr_lower in msd_attrs_lower:
                    #TODO controllo attr duplicati
                    #gestione attr duplicati in lista per pos
                    if attr_lower == 'ind' and i == 1:
                        continue
                    if attr_lower == 'imp' and i == 2:
                        continue
                    #setta nella lista attrs da esportare l'attr di riga
                    #alla posizione del nome msd corrispondente
                    idx = self.corpus_msd_lst.index(msd_name)
                    row_msds[idx] = attr
                    break
        print(row_msds)
        input('.')
        return row_msds

    # aggiunge le sigle ordinate alla row e inserisce attrs
    # aggiunge località e data deelle sigle dei testimoni
    def build_row(self, r):

        #sigle della riga
        r_sgs = r[SIGLA].split(',')
        r_sgs = [x for x in r_sgs if x != '']

        #distribuisce le sigle di riga nella lista delle sigle del corpus
        row_sgs = [x if x in r_sgs else '' for x in self.corpus_sgs]

        #attributi di riga escluso '' e resi minuscoli
        row_attrs = r[MSD].split(',')
        row_attrs = [x for x in row_attrs if x != '']

        pos = r[POS].lower()
        if pos == '':
            return None

        #assenazione valori attributi alle colonne msd
        row_msds = self.build_row_msd(pos, row_attrs)

        # separazione loc, data in  LANG
        l_d = f"{r[LANG]},,".split(',')
        lang = l_d[0]
        data = l_d[1]

        #assegnazione pos_name
        pos_name = self.pos_msd_json[pos]['pos_name']

        #aggiunta località e date testimone
        row_loc_dat = self.build_row_loc_dat(r_sgs)

        #["FORMA", "LEMMA", "ETIMO", "LANG", "POS", "FUNCT"],MSDS,SIGLE ..,LOC,DATE..
        row_exp = [
            r[FORMA], r[LEMMA], r[ETIMO], lang, data, pos_name, r[FUNCT]
        ] + row_msds + row_sgs + row_loc_dat
        return row_exp

    def export_corpus(self):
        corpus_path = os.path.join(CORPUS_DIR, CORPUS_NAME)
        rows = []
        try:
            with open(corpus_path, 'r', encoding=ENCODING) as f:
                reader = csv.reader(f, delimiter='|')
                for row in reader:
                    rows.append(row)
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
        #tabella conversione sigla dta,loc
        self.read_exp_csv()

        try:
            fw = open(exp_path, "w", encoding=ENCODING)
            writer = csv.writer(fw, delimiter='|')

            # head
            #intestazione comprensiva delle sigle e msd
            # TODO msd maiuscole
            # attrs_head = [x.upper() for x in self.corpus_msd_lst]
            attrs_head = self.corpus_msd_lst
            # FORMA,LEMMA,ETIMO,LANG,DATTE,POS,FUNCT,msda,...,loc,...,date,...
            head = [
                "FORMA", "LEMMA", "ETIMO", "LANG", "DATE", "POS", "FUNCT"
            ] + attrs_head + self.corpus_sgs + self.head_locs + self.head_dates
            writer.writerow(head)

            #scrittura rows
            rows.sort()
            for row in rows:
                r = self.build_row(row)
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
        tab12_name = text_name.replace(".txt", f".{self.exp_name}.csv")
        tab12_path = os.path.join(DATA_EXPORT_DIR, tab12_name)
        print(tab12_path)
        tab1 = pd.read_csv(token_path, delimiter='|', header=None)
        tab2 = pd.read_csv(form_path, delimiter='|', header=None)

        # TODO trasformazione minuscolo
        # tab1 = tab1.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        # tab2 = tab2.applymap(lambda x: x.lower() if isinstance(x, str) else x)

        formakey = tab2[1].duplicated().any()
        if formakey:
            print("La chiave formaskey non è unica.")
        tab1 = tab1.rename(columns={1: 'col2'})
        tab2 = tab2.rename(columns={1: 'col2'})
        tab12 = pd.merge(tab1, tab2, on='col2', how='left')
        tab12 = tab12.drop(tab12.columns[[1, 2]], axis=1)
        tab12[''] = self.text_sigla
        tab12 = tab12.fillna('')
        #attrs in minuscolo
        tab12.iloc[:, 6] = tab12.iloc[:, 6].str.lower()

        # tab12[[3, 4]] = tab12[3].str.split(',', expand=True)
        # tab12 = tab12.drop(3, axis=1)

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
        names = self.read_text_list()
        # for name in names:
        #     if name.strip() == '':
        #         continue
        #     self.text_sigla = name.split('.')[-1:][0]
        #     text_name = name + ".txt"
        #     self.export_token_form(text_name)
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
