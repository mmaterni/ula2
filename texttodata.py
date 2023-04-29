#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
from ulalib.ualog import Log
import ulalib.pathutils as ptu
from ulalib.ula_setting import *

__date__ = "17-04-2023"
__version__ = "0.3.9"
__author__ = "Marta Materni"


class Text2Data(object):
    """
    text2data(text_path) 
    estrai dati li scrive in formato csv
    aggiorna data/text_list.txt
    
    es.
    txt_path =   text_src/<name_file>.txt

    estrae i dati e scrive in
    data/<name_file>.form.csv
    data/<name_file.token.csv
    # aggorna
    # data/text_lst.txt
    """

    def __init__(self):
        path_err = "log/text2data.ERR.log"
        self.logerr = Log("w").open(path_err, 1).log

    def text2token_list(self, text):
        # AAA mantenimento verso
        # text = text.replace(os.linesep, ' ')
        tknew_line=" ## "
        text = text.replace(os.linesep,tknew_line)
        lst = re.split(" ", text)
        token_lst = []
        for token in lst:
            token = token.strip()
            if token == '':
                continue
            token = token.lower()
            s = f"{token}|{token}"
            token_lst.append(s)
        return token_lst

    def token_list2form_list(self, token_lst):
        #lst = sorted(list(set(token_lst)))
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

    # scrive data/text_name.form.csv
    #        data/txt_name.token.csv
    def write_tokens_forms(self, f_inp):
        try:
            fr = open(f_inp, 'r', encoding=ENCODING)
            text = fr.read()
            fr.close()
        except Exception as e:
            msg = f'ERROR 1 write_tokens_forms \n{e}'
            self.logerr(msg)
            sys.exit()

        token_lst = self.text2token_list(text)
        form_lst = self.token_list2form_list(token_lst)
        file_name = os.path.basename(f_inp)
        try:
            f_name_token = file_name.replace(".txt", ".token.csv")
            f_out = ptu.join(DATA_DIR, f_name_token).absolute()
            tokens = os.linesep.join(token_lst)
            ptu.make_dir_of_file(f_out)
            fw = open(f_out, "w", encoding=ENCODING)
            fw.write(tokens)
            fw.close()
        except Exception as e:
            msg = f'ERROR 2 write_tokens_forms \n{e}'
            self.logerr(msg)
            sys.exit()
        print(f"{f_inp} =>\n{f_out}")

        try:
            f_name_form = file_name.replace(".txt", ".form.csv")
            f_out = ptu.join(DATA_DIR, f_name_form).absolute()
            forms = os.linesep.join(form_lst)
            ptu.make_dir_of_file(f_out)
            fw = open(f_out, "w", encoding=ENCODING)
            fw.write(forms)
            fw.close()
        except Exception as e:
            msg = f'ERROR 3 write_tokens_forms \n{e}'
            self.logerr(msg)
            sys.exit()
        print(f"{f_inp} =>\n{f_out}")

    # def write_text_list(self):
    #     try:
    #         src = ptu.str2path(DATA_DIR)
    #         file_text_lst = ptu.list_path(src, "*.form.csv")
    #         text_lst = sorted([x.name.replace(".form.csv", "")
    #                           for x in file_text_lst])
    #         text = os.linesep.join(text_lst)
    #         ptu.make_dir_of_file(TEXT_LIST_PATH)
    #         fw = open(TEXT_LIST_PATH, "w", encoding=ENCODING)
    #         fw.write(text)
    #         fw.close()
    #     except Exception as e:
    #         msg = f'ERROR write_text_list \n{e}'
    #         self.logerr(msg)
    #         sys.exit(e)

    def text2data(self, text_path):
        self.write_tokens_forms(text_path)
        # self.write_text_list()


def do_main(text_path):
    Text2Data().text2data(text_path)


if __name__ == "__main__":
    le = len(sys.argv)
    if le < 2:
        print(f"\nauthor: {__author__}")
        print(f"release: {__version__} { __date__}")
        h = """ 
texttodata.py <text_path>
        """
        print(h)
        sys.exit()
    text_path = sys.argv[1]
    do_main(text_path)
