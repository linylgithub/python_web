#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 六  1/ 5 16:58:02 2019
# File Name: kombu_consumer.py
# Description:
"""

from kombu import Connection, Exchange, Queue, Consumer
from kombu.async import Hub

web_exchange = Exchange('web_develop', 'direct', durable=True)
standard_queue = Queue('standard', exchange=web_exchange, routing_key='web.develop')
URI = 'librabbitmq://linyl:123456@localhost:5672/web_develop'
hub = Hub()

def on_message(body, message):
    print("Body: '%s', Properties: '%s', DeliveryInfo: '%s'"%(body, message.properties, message.delivery_info))
    message,ack()

with Connection(URI) as connection:
    connection.register_with_event_loop(hub)
    with Consumer(connection, standard_queue, callback=[on_message]):
        try:
            hub.run_forver()
        except KeyboardInterrupt:
            exit(1)
