#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from ulalib.test_ula import TestUla

# es tr000.txt
if __name__ == "__main__":
    if(len(sys.argv))> 1:
        text_name = os.path.sys.argv[1]
        ut=TestUla()
        ut.text_corpus_diff(text_name)
    else:
        ut=TestUla()
        ut.diff_all()
