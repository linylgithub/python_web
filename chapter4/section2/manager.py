#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : Fri Nov 23 16:12:59 2018
# File Name: manager.py
# Description:
"""

from flask_script import Manager, Server, Shell, prompt_bool
from app import app, db, PasteFile

manager = Manager(app)

def make_shell_context():
    return {
        'db': db,
        'PasteFile': PasteFile,
        'app': app
    }

@manager.command
def dropdb():
    if prompt_bool(
        'Are you sure want to lose all your data'):
        db.drop_all()
    

@manager.option('-h', '--filehash', dest='filehash')
def get_file(filehash):
    paste_file = PasteFile.query.filter_by(filehash=filehash).first()
    if not paste_file:
        print 'Not file exists'
    else:
        print 'URL is {}'.format(paste_file.get_url('i'))
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(
    use_debugger=True, use_reloader=True,host='0.0.0.0', port=9000)
    )

if __name__ == '__main__':
    manager.run()
    