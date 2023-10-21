#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pdb import set_trace
import sys
# import argparse
from ulalib.ualog import Log
import ulalib.pathutils as ptu
import pathlib as pth
# from ulalib.save_back import save_text_data_back
import shutil
import os
import re
from difflib import *
from ulalib.ula_setting import *
from texttodata import Text2Data
from textcleaner import TextCleaner
# from ulalib.update_data import UpdateData

__date__ = "19-01-2023"
__version__ = "0.2.3"
__author__ = "Marta Materni"

"""
Gestione testo modificato
"""
"""
    Prima di lanciare la procdure per le modifiche
    
    eseguire dal browser

    1) save data

    2) update corpus
 
    ------------------------------------------------
    
    lanciare la procedura textupd.py
    
    1) muove
       data/name.token.csv => tmp/name.token1.csv
       data/name.form.csv  => tmp/name.form1.csv

    2) elabora (add_text)
       data/name.token.csv
       data/name.form.csv

    3) muove
       data/name.token.csv => tmp/name.token2.csv
        
    4) elabora (set_diff)
        tmp/name.token3.csv
        tmp/name.form3.csv

    5) muove
       tmp/name.token3.csv => data/name.token.csv
       tmp/name.form3.csv  => data/name.form.csv
       stampa lista disamb.sovrascritti.
    
 ------------------------------------------------

    Per completare 
 
     eseguire daal browser
    
    1)load_data

    2) update_text

    3) sistemazione omografi disamb. sovrascritti
    
    4) update corpus

    token1: originale
    token2: modificato senza disambiguazione
    token3: corretto 

"""


class TextUpd(object):

    def __init__(self):
        path_err = "log/textupd.ERR.log"
        self.logerr = Log("w").open(path_err, 1).log

    def read_data(self, path):
        try:
            fr = open(path, 'r', encoding=ENCODING)
            text = fr.read()
            fr.close()
        except Exception as e:
            msg = f'ERROR {path} Not Found.\n{e}'
            self.logerror(msg)
            sys.exit(msg)
        text = text.replace(os.linesep, ' ')
        rows = re.split(" ", text)
        lst = []
        for row in rows:
            if row.strip() == '':
                continue
            lst.append(row)
        return lst

    def write_data(self, path, lst):
        try:
            text = os.linesep.join(lst)
            fw = open(path, "w", encoding=ENCODING)
            fw.write(text)
            fw.close()
        except Exception as e:
            msg = f'ERROR {path} \n{e}'
            self.logerror(msg)
            sys.exit(msg)

    def token_list2form_list(self, token_lst):
        lst = list(set(token_lst))
        form_lst = []
        for item in lst:
            if item.strip() == '':
                continue
            if item[0] in PUNCTS:
                continue
            if item[0].isnumeric():
                continue
            form = f'{item.strip()}||||||'
            form_lst.append(form)
        form_lst = sorted(form_lst, key=lambda x: (x.split('|')[0]))
        return form_lst

    def set_diff_token_list(self, lst1, lst2):
        d = Differ()
        diff = d.compare(lst1, lst2)
        diff_lst = list(diff)
        dlst = [x for x in diff_lst if len(x.strip()) > 0 and x[0] != '?']
        dlstda = [x for x in dlst if x[0] in ('-', '+', '^')]
        # self.write_data("tmp/diff.txt", dlst)
        
        upd_path="tmp/diff_upd.txt"
        self.write_data(upd_path, dlstda)
        s = open(upd_path, "r").read()
        print(f"\n\n{upd_path}")
        print(s)

        over_lst = []
        new_lst = []
        s_p = ""
        for r in dlst:
            s = r[1:].strip()
            if r.find("-") == 0:
                s_p = s
                continue
            if r.find("+") == 0 and len(s_p) > 1:
                f_p, k_p = s_p.split("|")
                if f_p != k_p:
                    f, k = s.split("|")
                    if f == f_p:
                        s = f'{f}|{k_p}'
                        over_lst.append(s)
            new_lst.append(s)
            s_p = ""

        over_path="tmp/diff_over.txt"
        self.write_data(over_path, over_lst)
        s = open(over_path, "r").read()
        print(f"\n\n{over_path}")
        print(s)

        return new_lst

    def set_diff(self, tkpath1, tkpath2, tkpath3, frpath3):
        tklst1 = self.read_data(tkpath1)
        tklst2 = self.read_data(tkpath2)
        tklst3 = self.set_diff_token_list(tklst1, tklst2)
        self.write_data(tkpath3, tklst3)

        # setta la lista delle form (vuote) fi tklst3
        frlst3 = self.token_list2form_list(tklst3)
        self.write_data(frpath3, frlst3)

    # def save_token_back(self, token_path):
    #     ymdh = str(datetime.datetime.today().strftime('%y%m%d_%H'))
    #     token_bak = token_path.replace(".csv", f"_{ymdh}.csv")
    #     shutil.copyfile(token_path, token_bak)

    # name.txt => name.token.csv
    def get_token_tmp_path(self, text_name, ext=""):
        token_name = text_name.replace(".txt", f".token{ext}.csv")
        token_tmp_path = os.path.join(TMP_DIR, token_name)
        return token_tmp_path

    # text/name.txt => data/name.token{ext}.csv
    def get_token_path(self, text_name):
        token_name = text_name.replace(".txt", f".token.csv")
        token_path = os.path.join(DATA_DIR, token_name)
        return token_path

    # name.token.csv => name.form.csv
    def token_to_formh(self, token_path, ext=""):
        form_path = token_path.replace(".token", ".form")
        return form_path

    def move_path(self, path1, path2):
        pth.Path(path2).unlink(missing_ok=True)
        shutil.move(path1, path2)

    def add_text(self, text_path, line_len=0):
        try:
            path_err = "log/addt_text.ERR.log"
            # logerr = Log("w").open(path_err, 1).log
            text_name = os.path.basename(text_path)

            # sistema il testo e salva
            out_path = ptu.join(TEXT_SRC_DIR, text_name)
            tcxclr = TextCleaner()
            tcxclr.clean_file_text(text_path, out_path, line_len)

            # estrae i dati csv e salva
            inp_path = out_path
            tx2dt = Text2Data()
            tx2dt.text2data(inp_path)
        except Exception as e:
            msg = f'ERROR add_text \n{e}'
            self.logerr(msg)
            sys.exit()

    def add_text_upd(self, text_path, line_len=0):
        text_name = os.path.basename(text_path)
        "text/name.txt => data/name.token.csv"
        tk_path = self.get_token_path(text_name)
        tk_path1 = self.get_token_tmp_path(text_name, "1")
        tk_path2 = self.get_token_tmp_path(text_name, "2")
        tk_path3 = self.get_token_tmp_path(text_name, "3")
        fr_path = self.token_to_formh(tk_path)
        fr_path1 = self.token_to_formh(tk_path1)
        fr_path3 = self.token_to_formh(tk_path3)

        # print(text_path)
        # print(text_name)
        # print(tk_path)
        # print(tk_path1)
        # print(tk_path2)
        # print(tk_path3)
        # print(fr_path)
        # print(fr_path1)
        # print(fr_path3)

        # if ptu.exists(token_path) is False:
        if pth.Path(tk_path).exists() is False:
            print(f"\n\n{tk_path} Non  esistente")
            print("Lanciare prima textadd.py con il testo originale")
            sys.exit()
        # set_trace()
        # crea se non esiste la dir tmp
        # se esiste la svuota
        pth.Path(TMP_DIR).mkdir(exist_ok=True, mode=0o777)
        tmp_lst = [x for x in pth.Path(TMP_DIR).iterdir()]
        for path in tmp_lst:
            p = pth.Path(path)
            if p.is_file():
                p.unlink(path)
                print(f"{p}")

        # data/name.token.cv => tmp/name.token1.csv
        # data/name.form.cv => tmp/name.form1.csv
        self.move_path(tk_path, tk_path1)
        self.move_path(fr_path, fr_path1)

        # elabora e salva data/name.token.csv
        # data/name.token.csv => tmp/name.token2.csv
        self.add_text(text_path, line_len)
        self.move_path(tk_path, tk_path2)

        # salva rmp/name.token3.csv
        # salva rmp/name.form3.csv
        self.set_diff(tk_path1, tk_path2, tk_path3, fr_path3)

        # tmp/name.token3.csv => data/name.token.csv
        # tmp/name.form3.csv => data/name.form.csv
        self.move_path(tk_path3, tk_path)
        self.move_path(fr_path3, fr_path)

        #Aggiorna data/name.form.csv
        #con i dati di data_corpus/corpus.form.csv
        # upd = UpdateData()
        # upd.set_text_name(text_name)
        # upd.update_text_forms()


def do_main(text_path, ll):
    aut = TextUpd()
    aut.add_text_upd(text_path, ll)


if __name__ == "__main__":
    le = len(sys.argv)
    if le < 2:
        print(f"\nauthor: {__author__}")
        print(f"release: {__version__} { __date__}")
        h = """ 

textupd.py <text_path>
        """
        print(h)
        sys.exit()
    text_path = sys.argv[1]
    line_len = 0 if le < 3 else sys.argv[2]
    n = int(line_len)
    do_main(text_path, n)
