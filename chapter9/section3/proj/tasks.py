#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 三  1/ 2 17:32:40 2019
# File Name: tasks.py
# Description:
"""

from __future__ import absolute_import

from proj.celery import app

@app.task
def add(x, y):
    return x + y

