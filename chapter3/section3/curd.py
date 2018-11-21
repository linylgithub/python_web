#! /usr/bin/env python
# coding=utf-8

import MySQLdb
from consts import HOSTNAME, DATABASE, USERNAME, PASSWORD

con = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)

with con as cur:
    cur.execute('drop table if exists users')
    cur.execute('create table users(ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))')
    cur.execute("insert into users (Name) values('xiaolin')")
    cur.execute("insert into users (Name) values('xiaozhang')")
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    for row in rows:
        print row
    cur.execute("update users set Name=%s where Id=%s", ('yang',2))
    print 'Number of rows updates:', cur.rowcount

    cur = con.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from users")

    rows = cur.fetchall()
    for row in rows:
        print row['ID'], row['Name']

