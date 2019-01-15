#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 四  1/10 16:32:18 2019
# File Name: gevent_spawn.py
# Description:
"""

import gevent

def a():
    print 'Start a'
    gevent.sleep(1)
    print 'End a'

def b():
    print 'Start b'
    gevent.sleep(2)
    print 'End b'

gevent.joinall([
    gevent.spawn(a),
    gevent.spawn(b),
    ])
