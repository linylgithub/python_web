#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 三  1/ 2 17:34:18 2019
# File Name: celeryconfig.py
# Description:
"""
from kombu import Queue

BROKER_URL = 'amqp://linyl:123456@localhost:5672/web_develop' # 使用rabbitmq作为消息代理
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # 把任务结果存在了redis
CELERY_TASK_SERIALIZER = 'msgpack' # 任务序列化和反序列化使用msgpack方案
CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用可读性更好的json
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间， 不建议直接写86400， 应该让这样的magic数字表述更明显
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

CELERY_QUEUES = ( # 定义任务队列
        Queue('default', routing_key='task.#'), # 路由键以“task.“开头的消息都进default队列
        Queue('web_tasks', routing_key='web.#'), # 路由键以“web.”开头都消息都进web_tasks队列
        )
CELERY_DEFAULT_EXCHANGE = 'tasks' # 默认都交换机名字为tasks
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'  # 默认都交换类型是topic
CELERY_DEFAULT_ROUTING_KEY = 'task.default' # 默认都路由键是task.default，这个路由键符合上面都default队列
CELERY_ROUTES = {
        'projq.tasks.add': {    # task.add的消息会进入web_tasks队列
            'queue': 'web_tasks',
            'routing_key': 'web.add',
            }
        }
