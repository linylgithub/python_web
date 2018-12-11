#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 六 12/ 8 15:31:37 2018
# File Name: lastest_files_with_msgpack.py
# Description:
"""

import ast
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import msgpack


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://web:web123@120.79.248.110:3306/r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PasteFile(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5000), nullable=False)
    uploadtime = db.Column(db.DateTime, nullable=False)

    def __init__(self, name='', uploadtime=None):
        self.uploadtime = datetime.now() if uploadtime is None else uploadtime
        self.name

    def to_dict(self):
        d = {k: v for k, v in vars(self).items() if not k.startswith('_')}
        d['uploadtime'] = d['uploadtime'].strftime('%Y%m%d%H:%M:%S.%f')
        return str(d)

    @classmethod
    def from_dict(cls, data):
        data = ast.literal_eval(data)
        # id是自增长都字段，没有在__init__中传入，需要在生成对象之后再赋值id这个属性
        id = data.pop('id')
        data['uploadtime'] = datetime.strptime(data['uploadtime'], '%Y%m%d%H:%M:%S.%f')
        p = cls(**data)
        p.id = id
        return p

def default(obj):
    if isinstance(obj, PasteFile):
        return msgpack.ExtType(42, obj.to_dict())
    raise TypeError('Unknown type: %r' % (obj,))

def ext_hook(code, data):
    if code == 42:
        p = PasteFile.from_dict(data)
        return p
    return msgpack.ExtType(code, data)

p = PasteFile.query.get(100)
print p

packed = msgpack.packb(p, default=default)
print packed

unpacked = msgpack.unpackb(packed, ext_hook=ext_hook)
print unpacked

print unpacked.id, unpacked.name, unpacked.uploadtime
