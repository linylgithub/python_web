#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 三  1/ 2 17:34:18 2019
# File Name: celeryconfig.py
# Description:
"""

from datetime import timedelta

BROKER_URL = 'amqp://linyl:123456@localhost:5672/web_develop' # 使用rabbitmq作为消息代理
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # 把任务结果存在了redis
CELERY_TASK_SERIALIZER = 'msgpack' # 任务序列化和反序列化使用msgpack方案
CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用可读性更好的json
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间， 不建议直接写86400， 应该让这样的magic数字表述更明显
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

CELERYBEAT_SCHEDULE = {
    'add': {
        'task': 'projb.tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (16, 16)
    }
}

CELERY_SEND_TASK_SENT_EVENT = True
