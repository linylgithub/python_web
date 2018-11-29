#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 二 11/27 11:32:44 2018
# File Name: app.py
# Description:
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hellow'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
