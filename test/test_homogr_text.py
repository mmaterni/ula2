#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from ulalib.test_ula import TestUla


if __name__ == "__main__":
    if(len(sys.argv))> 1:
        text_name = os.path.sys.argv[1]
        ut=TestUla()
        ut.text_omogr(text_name)
    else:
        ut=TestUla()
        ut.text_omogr_all()
