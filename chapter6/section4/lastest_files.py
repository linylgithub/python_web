#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : Thu Nov 29 15:30:22 2018
# File Name: lastest_files.py
# Description:
"""
import json
from datetime import datetime

import redis
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://web:web123@120.79.248.110:3306/r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
r = redis.StrictRedis(host='120.79.248.110', port=6379, db=0)
MAX_FILE_COUNT = 50

class PasteFile(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5000), nullable=False)
    uploadtime = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, name='', uploadtime=None):
        self.uploadtime = datetime.now() if uploadtime is None else uploadtime
        self.name = name

db.create_all()

@app.route('/upload', methods=['POST'])
def upload():
    """上传"""
    name = request.form.get('name')
    pastfile = PasteFile(name=name)
    db.session.add(pastfile)
    db.session.commit()
    r.lpush('lastest.files', pastfile.id)
    r.ltrim('lastest.files', 0, MAX_FILE_COUNT)

    return jsonify({'r': 0})

@app.route('/lastest_files')
def get_lastest_files():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=20, type=int)
    ids = r.lrange('latest.files', start, start + limit - 1)
    files = PasteFile.query.filter(PasteFile.id.in_(ids)).all()
    return json.dumps([{'id': f.id, 'name': f.name} for f in files])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
