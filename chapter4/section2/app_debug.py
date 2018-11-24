#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : Fri Nov 24 16:15:59 2018
# File Name: app_debug.py
# Description:
"""

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'a secret key'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def hello():
    return "<body></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)