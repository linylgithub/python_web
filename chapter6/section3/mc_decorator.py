#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# Author: linyl
# Created Time : 二 11/27 17:12:25 2018
# File Name: mc_decorator.py
# Description: 实现一个叫作cache的装饰器，它可以方便地在方法上定义缓存键和缓存时间。
               cache需要一个格式化的函数，它可以把各种需要缓存的参数格式化成为一个缓存键
"""

import re
import time
import inspect
from functools import wraps

MC_DEFAULT_EXPIRE_IN = 0
__formaters = {}
percent_pattern = re.compile(r'%\w')
brace_pattern = re.compile(r'\{[\w\d\.\[\]_]+\}')


def formater(text):
    """sumary_line"""
    percent = percent_pattern.findall(text)
    brace = brace_pattern.findall(text)
    if percent and brace:
        raise Exception('mixed format is not allowed')

    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        print text
        return text.format

def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    print f
    return f(*a, **kw)

def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]
        
    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)

        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(' ', '_'), aa
    return gen_key

def cache(key_pattern, mc, expire=MC_DEFAULT_EXPIRE_IN, max_retry=0):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception('do not support varargs')
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a ,**kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            force = kw.pop('force', False)
            r = mc.get(key) if not force else None

            retry = max_retry
            while r  is None and retry > 0:
                # when node is down , add() will fialed
                if mc.add(key + '#mutex', 1, int(max_retry * 0.1)):
                    break
                time.sleep(0.1)
                r = mc.get(key)
                retry -= 1
            
            if r is None:
                r = f(*a, **kw)
                if r is not None:
                    mc.set(key, r, expire)
                if max_retry > 0:
                    mc.delete(key + '#mutex')
            return r
        _.original_function = f
        return _
    return deco

def create_decorators(mc):
    def _cache(key_pattern, expire=0, mc=mc, max_retry=0):
        return cache(key_pattern, mc, expire=expire, max_retry=max_retry)
    return {'cache': _cache}
    



if __name__ == '__main__':
    key = 'web_develop:users:%s'
    id_ = 1
    print format(key % '{id_}', id_=id_)
    n_key = 'web_develop:users:%s:%s'
    print format(n_key % ('{id_}','{type}'), id_=id_, type='a')
    def f(id_, type='aa', thh='hhh'):
        return id_, type
    arg_names, varargs, varkw, defaults = inspect.getargspec(f)
    print inspect.getargspec(f)
    print gen_key_factory(n_key, arg_names, defaults)(1)
    print gen_key_factory(n_key, arg_names, defaults)

