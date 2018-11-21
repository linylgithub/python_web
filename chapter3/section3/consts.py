#! /usr/bin/env python
# coding=utf-8

HOSTNAME = '120.79.248.110'
DATABASE = 'r'
USERNAME = 'web'
PASSWORD = 'web123'
DB_URI = 'mysql://{}:{}@{}/{}'.format(
        USERNAME, PASSWORD, HOSTNAME, DATABASE)


