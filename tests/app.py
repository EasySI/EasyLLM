#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@Project: EasyLLM
@File   : app.py
@Version: V1.0.0
@Author : WenC
@Time   : 2025-12-01 21:51:57
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2020-2030,Mr.WenC
@Desc   :
"""

# here put the import lib
import time
from celery import Celery

app = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/1',
    backend='redis://127.0.0.1:6379/2'
)


@app.task
def task(name, age):
    print(f"Ready to start task...")
    time.sleep(5)
    return f"Hello, My name is {name} and I am {age} years old!"
