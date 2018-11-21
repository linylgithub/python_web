#! /usr/bin/env python
# coding=utf-8

from sqlalchemy import create_engine
from consts import DB_URI

eng = create_engine(DB_URI)

with eng.connect() as con:
    con.execute('drop table if exists users')
    con.execute('create table users(ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))')
    con.execute("insert into users (Name) values('xiaolin')")
    con.execute("insert into users (Name) values('xiaozhang')")
    rows = con.execute("SELECT * FROM users")

    for row in rows:
        print row


