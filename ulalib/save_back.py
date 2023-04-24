#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from pdb import set_trace
import os
import shutil
import datetime
import sys
from ulalib.ula_setting import DATA_BACK_DIR, CORPUS_DIR, CORPUS_BACK_DIR
import ulalib.pathutils as ptu


def save_text_data_back(file_path):
    """
    file_path=/basedir/data/<name_file>.txt
    copia d il file 
    ./data/file.csv => ./data_bak/ymd/file_ymdh.txt
    """
    #ymd = str(datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S'))
    #ymd = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
    #ymd = str(datetime.datetime.today().strftime('%y%m_%H_%M'))
    ymd = str(datetime.datetime.today().strftime('%y%m%d'))
    ymdh = str(datetime.datetime.today().strftime('%y%m%d_%H'))
    back_dir = ptu.join(DATA_BACK_DIR, ymd)
    file_name = os.path.basename(file_path)
    file_name_back = file_name.replace(".csv", f"_{ymdh}.csv")
    file_path_back = os.path.join(back_dir, file_name_back)
    ptu.make_dir_of_file(file_path_back, 0o777)
    shutil.copyfile(file_path, file_path_back)
    # ptu.chmod(file_path_back,0o777)


def save_corpus_data_back(file_name):
    """
    file_name=corpus_name.form.csv
    copia d il file da 
    ./data_corpus/corpus_ame.form.csv 
    =>
    ./data_corpus_back/corpus_name_ymd.for.csv
    """
    ymd = str(datetime.datetime.today().strftime('%y%m%d'))
    ymdh = str(datetime.datetime.today().strftime('%y%m%d_%H'))
    back_dir = ptu.join(CORPUS_BACK_DIR, ymd)
    file_path = os.path.join(CORPUS_DIR, file_name)
    file_name_back = file_name.replace(".csv", f"_{ymdh}.csv")
    file_path_back = os.path.join(back_dir, file_name_back)
    ptu.make_dir_of_file(file_path_back, 0o777)
    if ptu.exists(file_path):
        shutil.copyfile(file_path, file_path_back)
        # ptu.chmod(file_path_back,0o777)


if __name__ == "__main__":
    if(len(sys.argv) > 1):
        path = sys.argv[1]
        save_text_data_back(path)
