#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ulalib.update_data import UpdateData
from ulalib.ula_setting import *
from ulalib.ualog import Log


log = Log("w").open("test.log", 1).log

class TestUla(object):

    def __init__(self):
        self.upd = UpdateData()

    def text_corpus_diff(self, text_name):
        log(f"{text_name}")
        self.upd.read_corpus_form_csv()
        self.upd.set_text_name(text_name)
        self.upd.read_text_form_csv()
        self.upd.set_text_flled_idx_lst()

        self.upd.set_text_corpus_diff_lst()
        for fc in self.upd.text_corpus_diff_lst:
            f, c =fc.split("$") 
            log(f)
            log(c)
            log("")

    def corpus_omogr(self):
        log("===> CORPUS_HOMOGR")
        self.upd.read_corpus_form_csv()
        self.upd.set_corpus_omogr_js()
        for k in self.upd.corpus_omogr_js.keys():
            fr=self.upd.corpus_omogr_js[k]
            # for fk in fr:
            #     r=", ".join(fk)
            #     log(r)
            # log("")
            fks=[]
            for fk in fr:
                fks.append(fk[1])
            r=", ".join(fks)
            log(r)

    #per ora invocato da test
    def text_omogr(self, text_name):
        log(f"==> {text_name}  HOMOGR")
        self.upd.read_corpus_form_csv()
        self.upd.set_text_name(text_name)
        self.upd.read_text_form_csv()
        self.upd.set_text_flled_idx_lst()
        self.upd.set_text_omogr_js()
        for k in self.upd.text_omogr_js.keys():
            fr=self.upd.text_omogr_js[k]
            fks=[]
            for fk in fr:
                fks.append(fk[1])
            r=", ".join(fks)
            log(r)

    def read_text_list(self):
        with open("./data/text_list.txt", "r") as f:
            lst = f.readlines()
        names = [x.strip()+".txt" for x in lst]
        return names

    #metodo da invocare manualmente
    def text_omogr_all(self):
        names = self.read_text_list()
        for name in names:
            self.text_omogr(name)

    # metodo da invocare manualmente
    def diff_all(self):
        log("TEXT DIFF CORPUS")
        log("row_text")
        log("row corpus\n")
        names = self.read_text_list()
        for name in names:
            self.text_corpus_diff(name)
