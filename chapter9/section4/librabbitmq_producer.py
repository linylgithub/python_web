#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 五  1/ 4 23:31:41 2019
# File Name: librabbitmq_producer.py
# Description:
"""

import sys
from librabbitmq import Connection

connection = Connection(host='localhost', userid='linyl', password='123456', virtual_host='web_develop')
channel = connection.channel()
channel.exchange_declare('web_develop', 'direct', passive=False, durable=True, auto_delete=False)
if len(sys.argv) != 1:
    msg = sys.argv[1]
else:
    msg = 'hello xiaolin'

channel.basic_publish(msg, 'web_develop', 'xxx_routing_key')
connection.close()
