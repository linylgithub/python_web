#! /usr/bin/env python
# coding=utf-8

from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, tuple_
from sqlalchemy.sql import select, asc, and_
from consts import DB_URI

engine = create_engine(DB_URI)

meta = MetaData(engine)

users = Table(
        'Users', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(50), nullable=False),
        )

if users.exists():
    users.drop()
users.create()

def execute(s):
    print '-' * 28
    rs = con.execute(s)
    for row in rs:
        print row['id'], row['name']

with engine.connect() as con:
    for username in ('zhangsan', 'wanglang', 'liuwu'):
        user = users.insert().values(name=username)
        con.execute(user)
    stm = select([users]).limit(1)
    execute(stm)

    k = [(2,)]
    stm = select([users]).where(tuple_(users.c.id).in_(k))
    execute(stm)

    stm = select([users]).where(and_(users.c.id > 2 ,users.c.id < 4))
    execute(stm)

    stm = select([users]).order_by(asc(users.c.name))
    execute(stm)
    stm = select([users]).where(users.c.name.like('%ang%'))
    execute(stm)

