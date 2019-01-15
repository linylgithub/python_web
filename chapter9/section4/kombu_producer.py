#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 六  1/ 5 13:23:22 2019
# File Name: kombu_producer.py
# Description:
"""

import sys

from kombu import Connection, Exchange, Queue, Producer

web_exchange = Exchange('web_develop', 'direct', durable=True)
standard_queue = Queue('standard', exchange=web_develop, routing_key='web.develop')
URI = 'librabbitmq://linyl:123456@localhost:5672/web_develop'

if len(sys.argv) > 1:
    msg = sys.argv[1]
else:
    msg = 'hello, kombu'

with Connection(URI) as connection:
    producer = Producer(connection)
    producer.publish(
            msg, exchange=web_exchange, declare=[standard_queue], routing_key='web.develop', serializer='json', compression='zlib')

