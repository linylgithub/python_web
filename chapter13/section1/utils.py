#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 三  1/ 9 18:02:51 2019
# File Name: utils.py
# Description:
"""

import random

import requests
from fake_useragent import UserAgent

from config import REFERER_LIST, TIMEOUT

def get_referer():
    return random.choice(REFERER_LIST)

def get_user_agent():
    ua = UserAgent(verify_ssl=False)
    return ua.random

def fetch(url, proxy=None):
    s = requests.Session()
    s.headers.update({'user-agent': get_user_agent()})

    proxies = None
    if proxy is not None:
        proxies = {
            'http': proxy,
        }
    return s.get(url, timeout=TIMEOUT, proxies=proxies)
