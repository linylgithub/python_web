#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : Sat Nov 24 21:46:46 2018
# File Name: app_security.py
# Description:
"""

from functools import wraps, reduce
from operator import or_

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_security import (
    Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required)
from flask_security.forms import LoginForm
from flask_security.utils import encrypt_password

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'login_user.html'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'

db = SQLAlchemy(app)


class Permission(object):
    """权限定义"""
    LOGIN = 0x01
    EDITOR = 0x02
    OPERATOR = 0x04
    ADMINISTER = 0xff
    PERMISSION_MAP = {
        LOGIN: ('login', 'Login user'),
        EDITOR: ('editor', 'Editor'),
        OPERATOR: ('op', 'Operator'),
        ADMINISTER: ('admin', 'Super administrator')
    }


# 用户权限关系表
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    """角色模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    permissions = db.Column(db.Integer, default=Permission.LOGIN)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """"用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def can(self, permissions):
        if self.roles is None:
            return False
        all_perms = reduce(or_, map(lambda x: x.permissions, self.roles))
        return all_perms & permissions == permissions

    def can_admin(self):
        return self.can(Permission.ADMINISTER)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=LoginForm)


@security.login_context_processor
def security_login_processor():
    print 'Login'
    return {}


@app.before_first_request
def create_user():
    """初始化"""
    db.drop_all()
    db.create_all()

    for permissions, (name, desc) in Permission.PERMISSION_MAP.items():
        user_datastore.find_or_create_role(
            name=name, description=desc, permissions=permissions
        )

    for email, passwd, permissions in (('linyl@gmail.com', '123', (Permission.LOGIN, Permission.EDITOR)),
                                       ('lisi@gmail.com', '123',
                                        (Permission.LOGIN,)),
                                       ('admin@gamil.com', 'admin', (Permission.ADMINISTER,))):
        user_datastore.create_user(
            email=email, password=encrypt_password(passwd))
        for permission in permissions:
            user_datastore.add_role_to_user(
                email, Permission.PERMISSION_MAP[permission][0])
    db.session.commit()


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def _deco(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return _deco
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


@app.route('/')
@login_required
@permission_required(Permission.LOGIN)
def index():
    return 'Login in'


@app.route('/admin/')
@login_required
@admin_required
def admin():
    return 'Only adminstrators can see this!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=app.debug)
