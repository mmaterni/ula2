#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# from ulalib.ula_setting import DATA_DIR
# import ulalib.pathutils as ptu


def save_data(filepath, data):
    root_dir = "/u/ulax/ula2"
    fpath = os.path.join(root_dir, filepath)
    fw = open(fpath, "wb")
    fw.write(data)
    fw.close()
    os.chmod(fpath, 0o777)
