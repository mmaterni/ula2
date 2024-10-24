#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sys

import ulalib.pathutils as ptu
from ulalib.ualog import Log
from ulalib.ula_setting import *

__date__ = "17-04-2023"
__version__ = "0.1.5"
__author__ = "Marta Materni"


class TextAdjust(object):
    """
    Sistema puteggiature
    rimuove spazi bianche maggiori di 1
    elimina spazi ad inizio e fine riga
    il parametro l (opzionale):
    -1) lascia la separazione originale
    0 ) separa per paragrafi
    >0) separa per lunghezza riga

    """

    def __init__(self):
        path_err = "log/text_cleaner.ERR.log"
        self.logerr = Log("w").open(path_err, 1).log

    def split_paragraph(self, text):
        text = text.replace(os.linesep, " ", -1)
        p_ln = "."+os.linesep
        text = re.sub(r"[\.][\s]{1,}", p_ln, text)
        return text

    def split_line(self, text, line_len):
        # sstituisce linessep con spazio
        text = text.replace(os.linesep, " ", -1)
        # elimina spazi multipli
        text = re.sub(r"[\s]{2,}", "", text)
        ls = []
        i = 0
        j = i + line_len
        while True:
            j = text.find(' ', j - 1)
            le = j - i
            if le > line_len:
                k = 1
                while True:
                    k += 1
                    if text[j - k] == ' ':
                        j = j - k
                        break
            s = text[i:j].strip()
            if s == '':
                break
            # print(s)
            # print(i, j, le, j - i, text[j - 1:j])
            ls.append(s + os.linesep)
            i = j
            j = i + line_len
        return "".join(ls)

    # # rimuove apostrofi
    # ptrn = r"\’\w"
    # lst = re.findall(ptrn, text)
    # lst = list(set(lst))
    # for ap in lst:
    #     ab = ap.replace("’", " ")
    #     # print(ap, ab)
    #     text = text.replace(ap, ab)
    # #
    # ptrn = r"\w'\w"
    # lst = re.findall(ptrn, text)
    # lst = list(set(lst))
    # for ap in lst:
    #     ab = ap.replace("'", " ")
    #     # print(ap, ab)
    #     text = text.replace(ap, ab)
    # pass


    def adjust_text(self, text, linebreak):
        # attaccare a sinistra
        # l’altra => l’ altra
        # attaccare a destra
        # de·l destrucion => de ·l destrucion
        # destruci-on => destruci -on
        PTR_CHS = [r"\s*[’]\s*",
                   r"\s*[-]\s*",
                   r"\s*[·]\s*"]
        CHS_LR = ['’'+BL,
                  BL+'-',
                  BL+'·']
        for x in zip(PTR_CHS, CHS_LR):
            ptr, ch = x
            text = re.sub(ptr, ch, text)

        # rimuove spazi multiplii
        pattern = r"[ ]{2,}"
        text = re.sub(pattern, " ", text)

        # attacca il punto a sinistra e mette uno spazio a destraa
        for p in list(".,;:!?"):
            text=text.replace(f" {p} ",f"{p} ")
            text=text.replace(f" {p}",f"{p} ")
       
        for p in list("’"):
            text=text.replace(f"{p} ",f"{p}")


        # rimuove line sep
        if linebreak == 0:
            pattern = r"[\n]+"
            text = re.sub(pattern, " ", text)
        # conserva line sep e rimuove spazi inizio riga
        else:
            pattern = r"[ ]*[\n][ ]* "
            text = re.sub(pattern, "\n", text)

        # rimuove spazi multiplii
        pattern = r"[ ]{2,}"
        text = re.sub(pattern, " ", text)

        # rimuove punti multipli
        # pattern = r"[\.]{2,}"
        # text = re.sub(pattern, ".", text)

        # rimuove virgole multiple
        # pattern = r'["]{2,}'
        # text = re.sub(pattern, '"', text)
        return text

    def adjust_file_text(self, in_path, out_path, line_len):
        lb = 1 if line_len < 0 else 0
        try:
            fr = open(in_path, 'r', encoding=ENCODING)
            text = fr.read()
            fr.close()
        except Exception as e:
            msg = f'ERROR 11 textadjust.py \n {e}'
            self.logerr(msg)
            sys.exit(e)
        try:
            text_clean = self.adjust_text(text, lb)
            if line_len > 0:
                text_src = self.split_line(text_clean, line_len)
            elif line_len == 0:
                text_src = self.split_paragraph(text_clean)
            else:
                text_src = text_clean
        except Exception as e:
            msg = f'ERROR 22 textcleaner.py \n {e}'
            self.logerr(msg)
            sys.exit(e)
        try:
            fw = open(out_path, 'w+', encoding=ENCODING)
            fw.write(text_src)
            fw.close()
            ptu.chmod(out_path, 0o777)
        except Exception as e:
            msg = f'ERROR 33 textadjust.py \n {e}'
            self.logerr(msg)
            sys.exit(e)
        print(f"{in_path} => {out_path}")


def do_main(in_path, out_path, line_len):
        TextAdjust().adjust_file_text(in_path, out_path, line_len)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print(f"\nauthor: {__author__}")
        print(f"release: {__version__} { __date__}")
        parser.print_help()
        sys.exit()
    parser.add_argument(
        '-i',
        dest="src",
        required=True,
        metavar="",
        help="-i <file.txt>")
    parser.add_argument(
        '-o',
        dest="out",
        required=True,
        metavar="",
        help="-o <fileclean.txt>")
    parser.add_argument(
        '-l',
        dest="linelen",
        required=False,
        default=-1,
        metavar="",
        help="-l <line length> -1:not split  0:paragraph >0:rows (default -1)")
    args = parser.parse_args()
    if args.src.lower() == args.out.lower():
        print("Files In Output Error!")
    else:
        ll = int(args.linelen)
        do_main(args.src, args.out, ll)
