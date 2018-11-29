#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 二 11/27 17:01:42 2018
# File Name: mv.py
# Description:
"""

from libmc import (
        Client, MC_HASH_MD5, MC_POLL_TIMEOUT, MC_CONNECT_TIMEOUT, MC_RETRY_TIMEOUT
        )
from mc_decorator import create_decorators

mc = Client(
        [
            'localhost',
            'localhost:11212',
            'localhost:11213 mc_213'
        ],
        do_split = True,
        comp_threshold = 0,
        noreply = False,
        prefix = None,
        hash_fn = MC_HASH_MD5,
        failover = False
    )

mc.config(MC_POLL_TIMEOUT, 100)
mc.config(MC_CONNECT_TIMEOUT, 300)
mc.config(MC_RETRY_TIMEOUT, 5)

globals().update(create_decorators(mc))
