#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 二  1/ 1 22:36:40 2019
# File Name: amqp_producer_with_confirm.py
# Description:
"""

import sys
import pika

# %2F是被转义的“/”，这里使用了默认的虚拟主机和默认的用户密码
parameters = pika.URLParameters('amqp://admin:admin@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters) # connection就是所谓的消息代理
channel = connection.channel() # 获取信道
# 声明交换机、指定交换机类型为直接交换。最后两个参数表示想要持久化的交换机，其中durable为True表示RabbitMQ在崩溃重启之后会重建队列和交换机
channel.exchange_declare(exchange='web_develop', exchange_type='direct', 
        passive=False, durable=True, auto_delete=False)
if len(sys.argv) != 1:
    msg = sys.argv[1]
else:
    msg = 'hah'

# 创建一个消息，delivery_mode为2表示让这个消息持久化，重启rabbitmq也不会丢失。使用持久化需要考虑为此付出的性能成本，如果开启此功能，强烈建议把消息存储在SSD上
props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
# basic_publish表示发送路由键xxx_routing_key，消息体为haha的消息给web_develop这个交换机
# 接收确认消息
channel.confirm_delivery()
if channel.basic_publish('web_develop', 'xxx_routing_key', msg, properties=props):
    print 'Message publish was confirmed'
else:
    print 'Mesage could not be confirmed'
connection.close() # 关闭连接

