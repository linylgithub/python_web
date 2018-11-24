#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: linyl
# Created Time : 三 11/21 10:05:28 2018
# File Name: utils.py
# Description:
"""

import os
import hashlib
from functools import partial

from config import UPLOAD_FOLDER

HERE = os.path.abspath(os.path.dirname(__file__))

def get_file_md5(f, chunk_size=8192):
    h = hashlib.md5()
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()

def humanize_bytes(bytesize, precision=2):
    abbrevs = (
            (1 << 50, 'FB'),
            (1 << 40, 'TB'),
            (1 << 30, 'GB'),
            (1 << 20, 'MB'),
            (1 << 10, 'KB'),
            (1, 'bytes')
        )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)

get_file_path = partial(os.path.join, HERE, UPLOAD_FOLDER)
