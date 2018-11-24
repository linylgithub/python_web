#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 三 11/21 10:32:18 2018
# File Name: ext.py
# Description:
"""

from flask_mako import MakoTemplates, render_template 
from flask_sqlalchemy import SQLAlchemy

mako = MakoTemplates()
db = SQLAlchemy()
