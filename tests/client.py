#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@Project: EasyLLM
@File   : client.py
@Version: V1.0.0
@Author : WenC
@Time   : 2025-12-01 22:23:06
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2020-2030,Mr.WenC
@Desc   :
"""

# here put the import lib
import time
from app import task

start = time.perf_counter()
task.delay("achilles", 17)
print(
    time.perf_counter() - start
)  #  0.04128062492236495