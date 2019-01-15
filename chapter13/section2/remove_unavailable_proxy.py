#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 四  1/10 16:36:12 2019
# File Name: remove_unavailable_proxy.py
# Description:
"""
from gevent.pool import Pool
from requests.exceptions import RequestException

from utils import fetch
from models import Proxy

pool = Pool(10)

def check_proxy(p):
    try:
        fetch('https://baidu.com', proxy=p['address'])
    except RequestException:
        print 
        p.delete()

pool.map(check_proxy, Proxy.objects.all())

