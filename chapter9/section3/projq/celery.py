#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 三  1/ 2 17:19:58 2019
# File Name: celery.py
# Description:
"""

from __future__ import absolute_import
from celery import Celery

app = Celery('projq', include=['projq.tasks'])
app.config_from_object('projq.celeryconfig')

if __name__ == '__main__':
    app.start()
