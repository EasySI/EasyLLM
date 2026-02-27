#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
@File   : __init__.py
@Version: v1.0.0
@Auther : WenC
@Time   : 2025-12-05 18:32:54
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2025-2035, Mr.WenC
@Desc   : 
"""

# here put the import lib
from typing import Any
from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def retrival(self, *args, **kwargs)-> Any:
        pass

    @abstractmethod
    def generic(self, *args, **kwargs)-> Any:
        pass

    @abstractmethod
    def graph(self, *args, **kwargs)-> Any:
        pass

    @abstractmethod
    def ser