#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import pprint
import json
from ulalib.ualog import Log

"""
legge dalla dir
pos.csv
msd.csv
produce il file
pos_msd.json
"""
__date__ = "15-11-2021"
__version__ = "0.1.0"
__author__ = "Marta Materni"


def pp(data, width=40):
    s = pprint.pformat(data, indent=2, width=width)
    return s


CSV_DELIMITER = '|'

DIR_CFG="./static/cfg"
POS_MSD_JSON = "pos_msd.json"

POS_NAME = 'pos_name'
MSD_IDS = 'msd_ids'
MSD_NAME = 'msd_name'
ATTRS = 'attrs'
MSD_LIST = 'msd_list'


class PosMsd2json(object):

    def __init__(self, dir_pos_msd):
        POS = "pos.csv"
        MSD = "msd.csv"
        self.path_pos_in = os.path.join(dir_pos_msd, POS)
        self.path_msd_in = os.path.join(dir_pos_msd, MSD)
        self.path_out = os.path.join(DIR_CFG, POS_MSD_JSON)

        path_info = "log/pos_msd.log"
        self.log_info = Log("w").open(path_info, 0).log
        path_err = "log/pos_msd.ERR.log"
        self.log_err = Log("w").open(path_err, 1).log

    def read_csv(self, path_csv):
        rows = []
        try:
            f = open(path_csv, "rt")
            for row in f:
                row = row.strip()
                if row == '':
                    continue
                if row[0] == '#':
                    continue
                fileds = row.split(CSV_DELIMITER)
                rows.append(fileds)
            f.close()
        except Exception as e:
            err = f'ERROR. read_csv() {path_csv}\n{e}'
            self.log_err(err)
            sys.exit(err)
        return rows

    # #name|sign|msd_id_list
    # adjective|ADJ|1,2,3,4
    def build_pos_json(self, rows):
        col_pos_name = 0
        col_pos_sign = 1
        col_pos_msd_ids = 2
        pos_js = {}
        for row in rows:
            sign = row[col_pos_sign]
            name = row[col_pos_name]
            msd_ids = row[col_pos_msd_ids:]
            if len(msd_ids) == 1 and msd_ids[0].strip() == '':
                msd_ids = []
            js = {
                POS_NAME: name,
                MSD_IDS: msd_ids
            }
            pos_js[sign] = js
        return pos_js

    # id|name|attrs
    # 1|gender|Fem,Masc
    def build_msd_json(self, rows):
        col_msd_id = 0
        col_msd_name = 1
        col_msd_attrs = 2
        msd_js = {}
        for row in rows:
            id = row[col_msd_id]
            name = row[col_msd_name]
            attrs = row[col_msd_attrs:]
            js = {
                MSD_NAME: name,
                ATTRS: attrs
            }
            msd_js[id] = js
        return msd_js

    # #name|sign|msd_id_list
    # adjective|ADJ|1,2,3,4
    #
    # id|name|attrs
    # 1|gender|Fem,Masc

    def build_json(self):
        pos_rows = self.read_csv(self.path_pos_in)
        pos_json = self.build_pos_json(pos_rows)
        pos = json.dumps(pos_json, indent=2, sort_keys=False)
        self.log_info(pos)

        msd_rows = self.read_csv(self.path_msd_in)
        msd_json = self.build_msd_json(msd_rows)
        msd = json.dumps(msd_json, indent=2, sort_keys=False)
        self.log_info(msd)

        pm_js = {}
        keys = pos_json.keys()
        for k in keys:
            v = pos_json[k]
            msd_ids = v['msd_ids']
            if msd_ids == []:
                ids = []
            else:
                ids = msd_ids[0].split(',')
            lst = []
            for msd_id in ids:
                try:
                    js = msd_json[msd_id]
                except KeyError as e:
                    msg = f'ERROR.\npos:{k} {pp(v)}\nmsd_id:{e} Not Found.'
                    self.log_err(msg).prn()
                    continue
                attrs = js.get(ATTRS, [])
                if len(attrs) > 0:
                    msd_attrs = attrs[0].split(',')
                else:
                    msd_attrs = []
                mjs = {
                    MSD_NAME: js[MSD_NAME],
                    ATTRS: msd_attrs
                }
                lst.append(mjs)
            pm_js[k] = {
                POS_NAME: v[POS_NAME],
                MSD_LIST: lst
            }
        pm = json.dumps(pm_js, indent=2, sort_keys=False)
        # pm = json.dumps(pm_js, separators=(',', ':'))
        with open(self.path_out, "w")as f:
            f.write(pm)
        os.chmod(self.path_out, 0o777)


def do_main(dir_pos_msd=DIR_CFG):
    PosMsd2json(dir_pos_msd).build_json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    do_main()
