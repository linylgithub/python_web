#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 五  1/ 4 23:44:07 2019
# File Name: librabbitmq_consumer.py
# Description:
"""

from librabbitmq import Connection

connection = Connection(host='localhost', userid='linyl', password='123456', virtual_host='web_develop')
channel = connection.channel()

def on_message(message):
    print("Body:‘%s', Properties:'%s', DeliveryInfo:'%s'"%(message.body, message.properties, message.delivery_info))
    message.ack()

channel.exchange_declare('web_develop', 'direct', passive=False, durable=True, auto_delete=False)
channel.queue_declare('standard', auto_delete=True)
channel.queue_bind('standard', 'web_develop', 'xxx_routing_key')
channel.basic_consume('standard', callback=on_message)


try:
    while True:
        connection.drain_events()
except KeyboardInterrupt:
    exit(1)

