#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 一 12/10 23:57:20 2018
# File Name: top_n.py
# Description:
"""

import string
import random

import redis

r = redis.StrictRedis(host='120.79.248.110', port=6379, db=0)
GAME_BOARD_KEY = 'game.board'

r.flushdb()
# 插入1000条随机用户名和分数组成的记录。zadd方法表示我们操作的是一个有序列表
for i in range(1000):
    score = round((random.random() * 100), 2)
    user_id = ''.join(random.sample(string.ascii_letters, 6))
    r.zadd(GAME_BOARD_KEY, score, user_id)

# 随机获得一个用户和他的得分，zrevrange表示从高到低对列表排序
user_id, score = r.zrevrange(GAME_BOARD_KEY, 0, -1,
        withscores=True)[random.randint(0, 200)]

print '------'
print user_id, score
print '-----'

board_count = r.zcount(GAME_BOARD_KEY, 0 , 100)
# 这个用户分数超过了多少用户
current_count = r.zcount(GAME_BOARD_KEY, 0, score)
print current_count, board_count

print 'TOP 10'
print '-' * 20
for user_id, score in r.zrevrangebyscore(GAME_BOARD_KEY, 100, 0, start=0,
        num=10, withscores=True):
    print user_id, score
