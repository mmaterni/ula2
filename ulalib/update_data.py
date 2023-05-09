#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
# import sys
import os
import json
from ulalib.ualog import Log
import ulalib.pathutils as ptu
from ulalib.ula_setting import CORPUS_NAME, DATA_DIR, CORPUS_DIR
from ulalib.ula_setting import ENCODING, TEXT_LIST_PATH

__date__ = "09-05-2023"
__version__ = "0.3.6"
__author__ = "Marta Materni"
"""
text form
amor|amor|lemma|etimo|lang|poas|func|msd
amor|amor2|lemma|etimo|lang|poas|func|msd

text token
amor|amor
amor|amor2

corpus form
amor|amor|lemma|etimo|lang|poas|func|msd|g,p,v
amor|amor2|lemma|etimo|lang|poas|func|msd|g,v

"""

FORMA = 0
FORMAKEY = 1
LEMMA = 2
ETIMO = 3
LANG = 4
POS = 5
FUNCT = 6
MSD = 7

SIGLA = 8

FORM_ROW_LEN = 8
CORPUS_ROW_LEN = 9


class UpdateData(object):
    """Aggiorna
    data/text_name.form.csv
    data_corpus/corpus_name.form.csv
    """

    def __init__(self):
        path_err = "log/UpdateData.ERR.log"
        self.logerr = Log("w").open(path_err, 1).log
        # sigla del teso
        self.sigla = "x"

        # lista di text_form.csv
        self.text_form_lst = []

        # lista degli idx di text_form settati
        # con almeno lemma=''
        self.text_filled_idx_lst = []

        # lista dell form di text filled diverse
        # dalle corrispondenti di corpus
        # individuate per formkey
        # itemm=[text_form,corpus_form]
        self.text_corpus_diff_lst = []

        # lista di corpus_form.csv
        self.corpus_form_lst = []

        # lista delle formkey di corpus
        # utilizzata per torvare idx utilizzando formkey
        self.corpus_formakey_lst = []

        # lesta delle form di corpus con formkey multiple
        # per disambiguazione
        # i0,i1, .. idx in corpuse delle formakey di form
        # ks={
        #  "forma":[[forma,formakei,'']
        #           forma,formakei,'']].
        self.corpus_omogr_js = {}
        # omografi nel testo
        self.text_omogr_js = {}

        # set path
        self.text_form_path = None

        corpus_name = CORPUS_NAME
        self.corpus_form_path = ptu.join(CORPUS_DIR, corpus_name)
        omogr_name = corpus_name.replace(".form.csv", "_omogr.json")
        self.corpus_omogr_path = ptu.join(CORPUS_DIR, omogr_name)

    def set_text_name(self, text_name):
        text_form_name = text_name.replace(".txt", ".form.csv")
        self.text_form_path = ptu.join(DATA_DIR, text_form_name)
        self.sigla = text_form_name.split('.')[1]

    def set_text_flled_idx_lst(self):
        """
        Popola
        liste degli indici dei text_form settati
        utilizza:
        self.text_form_lst
        setta:
            self.text_filled_idx_lst = []
        """
        self.text_filled_idx_lst = []
        for i, row in enumerate(self.text_form_lst):
            n = 0
            cols = row.split('|')
            if cols[LEMMA].strip() != "":
                n += 1
            # if text_form[ETIMO] == "":
            # if text_form[LANG] == "":
            # if cols[POS].strip() != "":
            #     n += 1
            # if text_form[FUNCT] == "":
            # if text_form[MSD] == "":

            # è sufficiente il lemma
            if n > 0:
                self.text_filled_idx_lst.append(i)

    def set_text_corpus_diff_lst(self):
        """Popola
        la lista dele coppie text_form, corpus_form
        settate diversamente
        itemm=[text_form,corpus_form]

        text   => amor|amor|lemma1|etimo|it.|NOUN|Noun|fem
        corpus => amor|amor|lemma|etimo|it.|NOUN|Noun|fem

        utilizza:
        self.text_form_lst
        self.text_filled_idx_lst
        self.corpus_formakey_lst
        self.corpus_form_lst
        setta e ritorna:
        self.text_corpus_diff_lst
        """
        self.text_corpus_diff_lst = []
        for idx in self.text_filled_idx_lst:
            text_row = self.text_form_lst[idx]
            text_cols = text_row.split('|')
            fk = text_cols[FORMAKEY]
            try:
                corpus_idx = self.corpus_formakey_lst.index(fk)
            except ValueError:
                corpus_idx = -1
            if corpus_idx < 0:
                continue
            corpus_row = self.corpus_form_lst[corpus_idx]
            corpus_cols = corpus_row.split('|')
            for tf, cf in zip(text_cols, corpus_cols):
                if tf != cf:
                    row = "$".join([text_row, corpus_row])
                    self.text_corpus_diff_lst.append(row)
                    break
        return self.text_corpus_diff_lst

    def set_corpus_omogr_js(self):
        """Popola
        la lista corpus_form con formkey omografe
        item=[forma,[i0, i1, .. ,in]]
        js={
            forma:[i0,i1, .. ,in]
        }
        utilizza:
        self.corpus_form_lst
        setta:
        corpus_omogr_js={
            "forma1"[
                [forma1,formakeylemma,etimo,..]
                [forma1,formakeylemma,etimo,..]
            ],
            "forma2"[
                [forma1,formakeylemma,etimo,..]
                [forma1,formakeylemma,etimo,..]
            ],
        """
        self.corpus_omogr_js = {}
        js = {}
        for i, row in enumerate(self.corpus_form_lst):
            cols = row.split('|')
            f = cols[FORMA]
            if f in js:
                js[f].append(i)
            else:
                js[f] = [i]

        for fr, i_s in js.items():
            if len(i_s) < 2:
                continue
            f_lst = []
            for i in i_s:
                row = self.corpus_form_lst[i].split('|')
                f_lst.append(row)
            self.corpus_omogr_js[fr] = f_lst

    #invocato solo da TEST
    def set_text_omogr_js(self):
        """Come mogr_js
        limitatamente a text_form corrente
        self.corpus_form_lst
        self.text_form_lst
        self.text_filled_idx_lst
        setta:
        text:omogr_js
        """
        self.text_omogr_js = {}
        self.set_corpus_omogr_js()
        frs = [fr.split('|')[0] for fr in self.text_form_lst]
        fr_set = set(frs)
        oks = self.corpus_omogr_js.keys()
        js = {}
        for k in oks:
            if k in fr_set:
                js[k] = self.corpus_omogr_js[k]
        self.text_omogr_js = js

    #################################
    # UPDATE
    ################################

    # forma, formakey, lemma, etimo, lang, pos, funct, msd
    # adonc|adonc||||||
    def update_text_forms(self):
        self.read_corpus_form_csv()
        self.read_text_form_csv()
        self.update_text_forms_lst()

    def update_text_forms_lst(self):
        """Aggiorna
        data/text_name.form.csv
        con i dati di data_corpus/corpus.form.csv
        AGGIORNA  LE FORM DI TEXT 
        utilizza:
        self.text_form_lst
        self.corpus_formakey_lst
        self.corpus_form_lst
        """
        for i, row in enumerate(self.text_form_lst):
            text_form = row.split('|')
            if len(text_form) < FORM_ROW_LEN:
                msg = "WARNING update_text_form\nrow:i}\n{row}\n{text_form}\n"
                self.logerr(msg)
                continue
            fk = text_form[FORMAKEY]
            try:
                # verifica se in corpus esiste formakey
                idx = self.corpus_formakey_lst.index(fk)
            except ValueError:
                idx = -1
            if idx < 0:
                continue
            corpus_row_sg = self.corpus_form_lst[idx]
            cols = corpus_row_sg.split("|")
            corpus_row = "|".join(cols[:FORM_ROW_LEN])
            self.text_form_lst[i] = corpus_row
        try:
            fw = open(self.text_form_path, "w", encoding=ENCODING)
            for row in self.text_form_lst:
                fw.write(row)
                fw.write(os.linesep)
            fw.close()
        except IOError as e:
            msg = f'ERROR update_text_form: \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)

    # forma, formakey, lemma, etimo, lang, pos, funct, msd
    def update_corpus_forms(self):
        """
        Aggiorna
        data_corpus/corpus_name.form.csv
        data_corpus/corpus_omogr.json

        con i dati di data/text_name.form.csv
        AGGIORNA SOOLO LE FORM PER LE QUALI
        lemma !='' '
        utilizza:
        self.text_form_lst
        self.text_filled_idx_lst

        self.corpus_formakey_lst
        self.corpus_form_lst

        aggiunge le righe nuove
        sovrascrive le righe modificate
        aggiorna le sigle del testi
        
        ritrona una lista delle variazioni nella forma
        riga__old$riga_nuova

        """
        self.read_text_form_csv()
        self.read_corpus_form_csv()
        self.set_text_flled_idx_lst()
        diff_lst = []
        # set_trace()
        for idx in self.text_filled_idx_lst:
            form_row = self.text_form_lst[idx]
            form_cols = form_row.split('|')
            fk = form_cols[FORMAKEY]
            try:
                # verifica se in corpus esiste formakey
                corpus_idx = self.corpus_formakey_lst.index(fk)
            except ValueError:
                corpus_idx = -1
            if corpus_idx < 0:
                # non esiste formakey
                # aggiunge form con sigla a corpus
                row_sg = form_row + "|" + self.sigla
                self.corpus_form_lst.append(row_sg)
            else:
                # esiste formakey nel corpus
                # modifica form di corpus a lo mette in lista
                # aggiungendo se necessario la sigla
                corpus_row_sg = self.corpus_form_lst[corpus_idx]
                cols = corpus_row_sg.split('|')
                corpus_row = "|".join(cols[:-1])
                #sigle del corpus
                sg = cols[SIGLA]
                sg_lst = sg.split(',')
                if not self.sigla in sg_lst:
                    sg_lst.append(self.sigla)
                    sg = ",".join(sg_lst)
                self.corpus_form_lst[corpus_idx] = form_row + "|" + sg
                if form_row != corpus_row:
                    row = form_row + "$" + corpus_row
                    diff_lst.append(row)

        #se manca una forma base la aggiunge con lemma=?
        f_lst = []
        fk_lst = []
        for form_row in self.corpus_form_lst:
            row = form_row.split('|')
            f_lst.append(row[FORMA])
            fk_lst.append(row[FORMAKEY])
        for f in f_lst:
            if not f in fk_lst:
                form_row = f"{f}|{f}|?||||||"
                self.corpus_form_lst.append(form_row)

        # scrittura corpus.form.csv
        try:
            ptu.make_dir_of_file(self.corpus_form_path)
            fw = open(self.corpus_form_path, "w", encoding=ENCODING)
            for form_row in self.corpus_form_lst:
                if form_row == "":
                    continue
                fw.write(form_row)
                fw.write(os.linesep)
            fw.close()
        except IOError as e:
            msg = f'ERROR update_corpus_form\n{e}\n'
            self.logerr(msg)
            raise Exception(msg)

        # elabora e salva corpus omografi
        self.set_corpus_omogr_js()
        s = json.dumps(self.corpus_omogr_js)
        try:
            fw = open(self.corpus_omogr_path, "w", encoding=ENCODING)
            fw.write(s)
            fw.close()
        except IOError as e:
            msg = f'ERROR corpus_omogrl_js:\n{e}\n'
            self.logerr(msg)
            raise Exception(msg)
        finally:
            #data = "\n".join(diff_lst)
            data = diff_lst
            # for x in data:
            #     ab = x.split('$')
            #     print(ab[0])
            #     print(ab[1] + "\n")
            return data

    ###################################
    # READ
    ###################################

    def read_text_form_csv(self):
        """Legge
        data/text_name.form.csv
        crea la lista delle form del testo
        setta:
        self.text_form_lst
        """
        self.text_form_lst = []
        try:
            with open(self.text_form_path, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
            for i, row in enumerate(lst):
                row = row.strip()
                if row == "":
                    break
                cols = row.split('|')
                if len(cols) < FORM_ROW_LEN:
                    msg = f"ERROR read_text_form_csv\n{self.text_form_path}\n{i}\n{row}\n{cols}\n"
                    self.logerr(msg)
                    continue
                self.text_form_lst.append(row)
        except Exception as e:
            msg = f'ERROR read_text_form_csv \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)

    def read_corpus_form_csv(self):
        """Legge
        data_corpus/corpus_name.form.csv
        crea la lista delle form e di formakey del corpus
        setta:
        self.corpus_form_lst
        self.corpus_formakey_lst
        """
        self.corpus_form_lst = []
        self.corpus_formakey_lst = []
        if not ptu.exists(self.corpus_form_path):
            return
        try:
            with open(self.corpus_form_path, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
            for i, row in enumerate(lst):
                row = row.strip()
                if row == "":
                    continue
                cols = row.split('|')
                if len(cols) < CORPUS_ROW_LEN:
                    msg = f"ERROR read_corpus_form\n{i}\n{row}\n{cols}\n"
                    self.logerr(msg)
                    continue
                self.corpus_form_lst.append(row)
                fk = cols[FORMAKEY]
                self.corpus_formakey_lst.append(fk)
        except Exception as e:
            msg = f'ERROR read_corpus_form_csv \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)

    def read_text_list(self):
        """Legge
        data_data/text_list.txt
        setta:
        self.text_lst
        """
        if not ptu.exists(TEXT_LIST_PATH):
            self.logerr("text_list.txt Not Found.").prn()
            return
        try:
            with open(TEXT_LIST_PATH, 'r', encoding=ENCODING) as f:
                lst = f.readlines()
        except Exception as e:
            msg = f'ERROR read_text_lst \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)
        names = [x.strip() for x in lst]
        return names

    def clear_text_form_lst(self):
        le = len(self.text_form_lst)
        for i in range(0, le):
            cols = self.text_form_lst[i].split("|")
            for j in range(2, FORM_ROW_LEN):
                cols[j] = ""
            row = ("|").join(cols)
            self.text_form_lst[i] = row

    def update_all_text_forms(self):
        """Aggiorna
        data/*.csv

        con i dati di data_corpus/corpus_name.form.csv
        AGGIORNA LE FORM DI TITTI ITEXT
        !!! PULISCE text_form e le setta con i dati
        di corpus_form_lstr

        utilizza:
        self.text_lst
        self.corpus_formakey_lst
        self.corpus_form_lst
        self.text_form_lst
        """
        self.read_corpus_form_csv()
        names = self.read_text_list()
        try:
            for text_name in names:
                print(text_name)
                text_form_name = text_name + ".form.csv"
                self.text_form_path = ptu.join(DATA_DIR, text_form_name)
                self.read_text_form_csv()
                self.clear_text_form_lst()
                self.update_text_forms_lst()
                # controlli
                # self.set_text_flled_idx_lst()
                # self.set_text_corpus_diff_lst()
                # print(text_name)
                # for idx in self.text_filled_idx_lst:
                #     row = self.text_form_lst[idx]
                #     print(row)

        except Exception as e:
            msg = f'ERROR update_all_text_forms \n{e}\n'
            self.logerr(msg)
            raise Exception(msg)
