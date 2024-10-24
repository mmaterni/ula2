#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import sys
from pdb import set_trace

import ulalib.pathutils as ptu
from textcleaner import TextCleaner
from texttodata import Text2Data
from ulalib.ula_setting import *

__date__ = "24-10-2024"
__version__ = "0.2.6"
__author__ = "Marta Materni"

class TextAdd(object):

    def __init__(self):
        pass

    def move_text2add(self,file_name):
        """
        sposta il file 
        text/file.loc.txt => text/add/file.loc.txt
        """
        text_dir = TEXT_DIR
        path_src = ptu.join(text_dir, file_name).absolute()
        text_add_dir = TEXT_BACK_DIR
        path_trg = ptu.join(text_add_dir, file_name).absolute()
        print(f"{path_src} =>\n{path_trg}")
        shutil.move(path_src, path_trg)


    def add_text_data(self,text_path, line_len):
        """
        pulisce il testo da file_path
        lo scrive TEXT_SRC_DIR
        esrae i dati 
        li scive in ./data
        pulisce file_path

        es.
        legge 
            ./text/file_nametxt
        TextCleaner pulisce dati e 
        scrive
            ./text_src/file_name.txt
        legge 
            ./text_src/file_nametxt
        Text2Data  estra i dati
        scrive 
        ./data/file_name.form.csv
        ./data/file_name.token.csv
        scrive
        ./data/text_list.txt

        """
        try:
            text_name = os.path.basename(text_path)
            text_path=ptu.join(TEXT_DIR,text_name).absolute()

            # sistema il testo e salva
            text_src_path=ptu.join(TEXT_SRC_DIR,text_name).absolute()
            tcxclr = TextCleaner()
            tcxclr.clean_file_text(text_path, text_src_path, line_len)

            # estrae i dati csv e salva
            tx2dt = Text2Data()
            tx2dt.text2data(text_src_path)
        except Exception as e:
            msg = f'ERROR \n{e}'
            sys.exit(msg)


    def write_text_list(self):
        try:
            path_names=ptu.list_path(TEXT_BACK_DIR,"*.txt")
            text_names=[x.name for x in path_names]
            text_names=[x.replace('.txt','') for x in text_names]
            text_names.sort()
            text_str = os.linesep.join(text_names)
            fw = open(TEXT_LIST_PATH, "w", encoding=ENCODING)
            fw.write(text_str)
            fw.close()
        except Exception as e:
            msg = f'ERROR write_text_list \n{e}'
            self.logerr(msg)
            sys.exit(e)


    def add_new_text_lst(self,line_len):
        text_patrh_lst=ptu.list_path(TEXT_DIR)
        for text_path in text_patrh_lst:
            text_name=text_path.name
            self.add_text_data(text_name, line_len)
            self.move_text2add((text_name))
            print("--")
        self.write_text_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    print(f"\nauthor: {__author__}")
    print(f"release: {__version__} { __date__}")
    parser.add_argument(
        '-l',
        dest="linelen",
        required=False,
        default='-1',
        metavar="",
        help='-l <line_length>(-1 default, 0:paragraph , n:line length')
    args = parser.parse_args()
    line_len = int(args.linelen)
    # line_len=70 #tagla a 70 caratteri
    # line_len=0 #tagla al paragrafo
    # line_len=-1 #conserva originale
    TextAdd().add_new_text_lst(line_len)
