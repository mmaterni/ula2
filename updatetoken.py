#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pdb import set_trace
import sys
import os
from difflib import SequenceMatcher
import pandas as pd

ULA_DATA_DIR = "ula_data"
DATA_DIR = f"{ULA_DATA_DIR}/data"
# DATA_BACK_DIR = f"{ULA_DATA_DIR}/data_back"
# TEXT_DIR = f"{ULA_DATA_DIR}/text"
# TEXT_BACK_DIR = f"{ULA_DATA_DIR}/text_back"
# TEXT_SRC_DIR = f"{ULA_DATA_DIR}/text_src"
TEXT_LIST_PATH = f'{ULA_DATA_DIR}/data/text_list.txt'
# CORPUS_NAME = f"corpus.form.csv"
# CORPUS_DIR = f"{ULA_DATA_DIR}/data_corpus"
# CORPUS_BACK_DIR = f"{ULA_DATA_DIR}/data_corpus_back"
DATA_RESTORED_DIR = f"{ULA_DATA_DIR}/data_restored"
# EXP_LOC_DAT_PATH = f"static/cfg/exp_loc_dat.csv"
# TMP_DIR = f"{ULA_DATA_DIR}/tmp"
# POS_MSD_CSV_PATH = "static/cfg/pos_msd.csv"
ENCODING = 'utf-8'
PUNCTS = ',.;::?!^~()[]{}<>=+*#@£&%/\\«»“"\'`‘'
PUN = "XX"
# PTR_CHS = [r"\s*[’]\s*", r"\s*[-]\s*", r"\s*[·]\s*"]
# CHS_LR = ['’' + BL, BL + '-', BL + '·']

SIMILITARY_MAX = 1.0
"""
Aggiorna gli omografi di u testo simile
"""


class UpdateToken(object):

    def __init__(self, similtary_ok="0.7"):
        self.similtary_ok = float(similtary_ok)
        self.model = None
        self.df0 = None,
        self.df1 = None,
        self.path_src = None,
        self.path_trg = None,
        self.rows0 = []
        self.fk_rows0 = []
        self.contest_delta = 8
        self.contest_lim = 5

    def set_context_lim(self, items, forma):
        #elimina la punteggiatura
        words = [x for x in items if not x[0] in PUNCTS]
        try:
            idx = words.index(forma)
        except ValueError as e:
            idx = -1
        if idx < 0:
            return []
        idx0 = max(idx - self.contest_lim, 0)
        idx1 = min(idx + self.contest_lim + 1, len(words))
        contest = words[idx0:idx1]
        return contest

    def fill_contest_rows(self, src_path):
        print(src_path)
        try:
            self.df0 = pd.read_csv(src_path, sep='|', header=None)
        except Exception as e:
            sys.exit(e)
        rows = self.df0.values
        le = len(rows)
        print("df0:", le)
        self.rows0 = []
        for i, row in enumerate(rows):
            forma = row[0]
            formakey = row[1]
            #lista delle formake per individuare  forma1,forma2,..
            self.fk_rows0.append([forma, formakey])
            if forma != formakey:
                idx0 = max(i - self.contest_delta, 0)
                idx1 = min(i + self.contest_delta + 1, le)
                items = rows[idx0:idx1]
                contest = [x[0] for x in items]
                contest_lim = self.set_context_lim(contest, forma)
                self.rows0.append(contest_lim)
            else:
                self.rows0.append([])

    def calc_similarity(self, row1, row2):
        try:
            rs = []
            for i, w1 in enumerate(row1):
                w2 = row2[i]
                matcher = SequenceMatcher(None, w1, w2)
                sim = matcher.ratio()
                rs.append(sim)
                # if sim != 1:
                #     print("{:<10} {:<10}  {}".format(w1, w2, sim))
            total = sum(rs)
            sim_row = total / len(rs)
        except Exception as e:
            print(e)
            input(".Error")
        return sim_row

    def calc_similarity_row(self, row1, row2):
        try:
            matcher = SequenceMatcher(None, row1, row2)
            sim_row = matcher.ratio()
        except Exception as e:
            print(e)
            input(".Error")
        return sim_row

    def calc_similarity_line(self, row1, row2):
        try:
            l1 = " ".join(row1)
            l2 = " ".join(row2)
            matcher = SequenceMatcher(None, l1, l2)
            sim_row = matcher.ratio()
        except Exception as e:
            print(e)
            input(".Error")
        return sim_row

    def update_token1(self, token_name):
        # AAA path = os.path.join(DATA_RESTORED_DIR, token_name)
        # setta la dir di destinazione del files modificto e de log
        path = os.path.join(DATA_DIR, token_name)
        print(path)
        self.path_trg = path
        try:
            self.df1 = pd.read_csv(path, sep='|', header=None)
        except Exception as e:
            sys.exit(e)
        rows1 = self.df1.values
        le = len(rows1)
        print("text:", le)

        similar_rows = []
        for i, row1 in enumerate(rows1):
            # AAA XXXif i > 100: break


            if i % 100 == 0:
                print(i)
            tk1_f = row1[0]
            if tk1_f[0] in PUNCTS:
                continue
            tk1_k = row1[1]
            row1_i = i

            i0 = max(i - self.contest_delta, 0)
            i1 = min(i + self.contest_delta + 1, le)
            fk_lst = rows1[i0:i1]
            # forma|key => forma
            f_lst = [x[0] for x in fk_lst]
            contest1 = self.set_context_lim(f_lst, tk1_f)
            #posizione della forma nel contest
            tk1_f_pos = contest1.index(tk1_f)
            contest1_len = len(contest1)
            # lista indici delle righe che contenfono
            # nella stessa posizione nel contesto

            # indices_found = [
            #     n for n, row in enumerate(self.rows0)
            #     if len(row) == contest1_len and tk1_f in row
            #     and row.index(tk1_f) == tk1_f_pos
            #     and self.fk_rows0[n][0] != self.fk_rows0[n][1]
            # ]
            indices_found = [
                n for n, row in enumerate(self.rows0)
                if self.fk_rows0[n][0] != self.fk_rows0[n][1] and len(row) ==
                contest1_len and tk1_f in row and row.index(tk1_f) == tk1_f_pos
            ]

            if len(indices_found) == 0:
                continue

            # selezona gli indici dell righe simili al contesto
            indices = []
            for i_found in indices_found:
                row0 = self.rows0[i_found]
                #  AAA
                # sim = self.calc_similarity(contest_forma, sentence)
                # sim = self.calc_similarity_row(token_contest, row_txt)
                sim = self.calc_similarity_line(contest1, row0)
                if sim > self.similtary_ok:
                    indices.append([i_found, sim])
                    if sim == SIMILITARY_MAX:
                        break
            if len(indices) == 0:
                continue
            # Trova l'elemento con il valore massimo d similitary nel secondo campo
            elem_max_sim = max(indices, key=lambda x: x[1])
            row0_i = elem_max_sim[0]
            sim = elem_max_sim[1]
            r = [row1_i, tk1_f, tk1_k, row0_i, sim, contest1]
            similar_rows.append(r)
        ###################
        self.log(similar_rows)
        for x in similar_rows:
            row1_i = x[0]
            row0_i = x[3]
            t_k0 = self.df0.iat[row0_i, 1]
            row1_i = x[0]
            self.df1.iat[row1_i, 1] = t_k0

        #scrittura file tiken
        """
        read
        ula_data/data/<src>.token.csv
        wrute
        ula_data/data/<trg>.token.csv
        ula_data/data/<trg>.form.csv
        """

        print("\n")
        print(self.path_src)
        print("...")
        # print(self.path_trg)
        # AAA path = self.path_trg.replace(".csv", "_upd.csv")
        path = self.path_trg
        print(path)
        self.df1.to_csv(path, sep="|", index=False, header=False)
        self.log_udated(rows1)

        #scrittura file form
        #AAA path = path.replace(".token_upd.", ".form_upd.")
        path = path.replace(".token.", ".form.")
        print(path)
        forms = self.token_list2form_list(rows1)
        self.write_list(path, forms)
        print(self.path_word_log)
        print(self.path_row_log)

    def token_list2form_list(self, rows1):
        csv = [f"{x[0]}|{x[1]}" for x in rows1]
        lst = list(set(csv))
        form_lst = []
        # set_trace()
        for item in lst:
            if item.strip() == "":
                continue
            row = item.split('|')
            f = row[0]
            if f == "":
                continue
            if f in PUNCTS:
                continue
            if f.isnumeric():
                continue
            if f[0].isdigit():
                continue
            k = row[1]
            form = f"{f}|{k}||||||"
            form_lst.append(form)
        # set_trace()
        form_lst = sorted(form_lst, key=lambda x: (x.split('|')[1]))
        return form_lst

    def write_list(self, path, rows):
        with open(path, "w") as f:
            for x in rows:
                f.write(x)
                f.write(os.linesep)
        os.chmod(path, 0o666)

    def log_udated(self, rows1):
        #AAA path = self.path_trg.replace(".csv", "_upd.x.log")
        path = self.path_trg.replace(".csv", ".word.log")
        self.path_word_log=path
        f = open(path, "w")
        for i, x in enumerate(rows1):
            if x[0] != x[1]:
                s = "{:<7}{:<15}{:<15}\n".format(i, x[0], x[1])
                f.write(s)
        f.close()

    def log(self, similar_rows):
        #AAA path = self.path_trg.replace(".csv", "_upd.y.log")
        path = self.path_trg.replace(".csv", ".row.log")
        self.path_row_log=path
        f = open(path, "w")
        for x in similar_rows:
            row1_i = x[0]
            tk1_f = x[1]
            row0_i = x[3]
            sim = x[4]
            # token_k = row[2]
            # f.write(s)
            # tk0_f = self.df0.iat[row0_i, 0]
            tk0_k = self.df0.iat[row0_i, 1]
            # s = f"{tk0_f}   {tk0_k}\n"
            s = "\n{:<15} {:<15} {}\n".format(tk1_f, tk0_k, round(sim, 4))
            f.write(s)
            contest1 = " ".join(x[5])
            # f.write(f"{row1_i} {contest1}\n")
            f.write("{:<6}{}\n".format(row1_i, contest1))
            row0 = self.rows0[row0_i]
            row0 = " ".join(row0)
            # f.write(f"{row0_i} {row0}\n")
            f.write("{:<6}{}\n".format(row0_i, row0))
        f.close()

    def update(self, name_src, name_trg):
        name_src = os.path.basename(name_src)
        token_name = f"{name_src}.token.csv"
        src_path = os.path.join(DATA_DIR, token_name)
        self.path_src = src_path
        self.fill_contest_rows(src_path)

        name_trg = os.path.basename(name_trg)
        token_name = f"{name_trg}.token.csv"
        self.update_token1(token_name)


def do_main(src, trg, sim):
    rd = UpdateToken(sim)
    rd.update(src, trg)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("updatetoken.py <testo_src> >testo_target> [similtary]")
        es = """

es.
updatetoken.py tr1.g tr1.p 0.7
updatetoken.py testo1.g testo4.g 0.6

il primo testo è quello lavorato, il secondo
quello nel quale aggiungere ai token le forme 
per la disiambiguazione.
Il coefficienti similtary è per default = 0.7

"""
        print(es)
        sys.exit(0)
    src = sys.argv[1]
    trg = sys.argv[2]
    sim = 0.7
    if len(sys.argv) > 3:
        sim = sys.argv[3]
    do_main(src, trg, sim)
