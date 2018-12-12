#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 二 12/11 22:12:05 2018
# File Name: user_active.py
# Description:
"""

import time
import random
from datetime import datetime

import redis

ACCOUNT_ACTIVE_KEY = 'account:active'

r = redis.StrictRedis(host='120.79.248.110', port=6379, db=0)

r.flushall()
now = datetime.utcnow()

def record_active(account_id, t=None):
    if t is None:
        t = datetime.utcnow()
    p = r.pipeline()  # 使用Redis提供的事务
    key = ACCOUNT_ACTIVE_KEY
    for arg in ('year', 'month', 'day'):
        key = '{}:{}'.format(key, getattr(t, arg))
        p.setbit(key, account_id, 1) # 设置年月日三种键
    p.execute()  # 事务提交


def gen_records(max_days, population, k):  # 随机生成一些数据
    for day in range(1, max_days): # 日期需要从1开始
        time_ = datetime(now.year, now.month, day)
        accounts = random.sample(range(population), k)
        for account_id in accounts:
            record_active(account_id, time_)

def calc_memory():
    r.flushall()

    print 'USED_MEMORY: {}'.format(r.info()['used_memory_human'])
    start = time.time()
    print datetime.now()
    # 20 * 100000次（100万中选10万）
    gen_records(21, 1000000, 100000)
    print 'COST: {}'.format(time.time() - start)  # 记录花费时间
    print 'USED_MEMORY: {}'.format(r.info()['used_memory_human'])
    print datetime.now()

if __name__ == '__main__':
    calc_memory()
    print '这个月总的活跃人数：'
    print r.bitcount('{}:{}:{}'.format(ACCOUNT_ACTIVE_KEY, now.year, now.month))
    print '今天的活跃用户数：'
    print r.bitcount('{}:{}:{}:{}'.format(ACCOUNT_ACTIVE_KEY, now.year, now.month,
        now.day))




