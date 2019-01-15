#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 四  1/10 15:05:49 2019
# File Name: proxy_fetcher_with_queue.py
# Description:
"""
import re
import Queue
import threading

import requests
from mongoengine import NotUniqueError

from models import Proxy
from config import PROXY_REGEX, PROXY_SITES
from utils import fetch

def save_proxies(url):
    proxies = []
    try:
        r = fetch(url)
    except requests.exceptions.RequestException:
        return False
    addresses = re.findall(PROXY_REGEX, r.text)
    for address in addresses:
        proxy = Proxy(address=address)
        try:
            proxy.save()
        except NotUniqueError:
            pass
        else:
            proxies.append(address)

    return proxies


def cleanup():
    Proxy.drop_collection()


def save_proxies_with_queue(queue):
    while True:
        url = queue.get()
        save_proxies(url)
        queue.task_done()   # 向任务已经完成的队列发送一个信号


def use_thread_with_queue():
    cleanup()
    queue = Queue.Queue()

    for i in range(5):
        t = threading.Thread(target=save_proxies_with_queue, args=(queue,))
        t.setDaemon(True)
        t.start()

    for url in PROXY_SITES:
        queue.put(url)

    queue.join()


def save_proxies_with_queue2(in_queue, out_queue):
    while True:
        url =in_queue.get()
        rs = save_proxies(url)
        out_queue.put(rs)
        in_queue.task_done()   # 向任务已经完成的队列发送一个信号


def append_result(out_queue, result):
    while True:
        rs = out_queue.get()
        if rs:
            result.extend(rs)
        out_queue.task_done()


def use_thread_with_queue2():
    cleanup()
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()

    for i in range(5):
        t = threading.Thread(target=save_proxies_with_queue2, args=(in_queue, out_queue))
        t.setDaemon(True)
        t.start()

    for url in PROXY_SITES:
        in_queue.put(url)

    results = []

    for i in range(5):
        t = threading.Thread(target=append_result, args=(out_queue, results))
        t.setDaemon(True)
        t.start()

    in_queue.join()
    out_queue.join()

    print len(results)

if __name__ == "__main__":
    use_thread_with_queue2()
