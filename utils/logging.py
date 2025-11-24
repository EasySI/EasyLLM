#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File   : logging.py
@Version: v1.0.0
@Author : WenC
@Time   : 2025-11-24 22:20:28
@Email  : mr.wenc2640@gmail.com
@License: (C)Copyright 2025-2035, WenC
@Desc   : 
"""

# here put the import libs
import os
import logging
from threading import Lock
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler


class Singleton(type):
    """单例元类"""
    _lock = Lock()
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # 以application name 为单例 key （第一个参数 application）
        key = (cls, args, args[0] if args else None)

        if key not in cls._instances:
            with cls._lock:
                if key in cls._instances:
                    return cls._instances[key]

                cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[key]


class ColoredFormatter(Formatter):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"
    COLORS = {
        'WARNING': BLUE,
        'INFO': YELLOW,
        'DEBUG': GREEN,
        'CRITICAL': MAGENTA,
        'ERROR': RED,
        'RED': RED,
        'GREEN': GREEN,
        'YELLOW': YELLOW,
        'BLUE': BLUE,
        'MAGENTA': MAGENTA,
        'CYAN': CYAN,
        'WHITE': WHITE,
    }

    def __init__(self, *args, **kwargs):
        Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        level_name = record.levelname
        color = self.COLOR_SEQ % (30 + self.COLORS[level_name])
        message = Formatter.format(self, record)
        message = message.replace("$RESET", self.RESET_SEQ) \
            .replace("$BOLD", self.BOLD_SEQ).replace("$COLOR", color)
        return message + self.RESET_SEQ


class Logger(logging.Logger, metaclass=Singleton):
    log_stderr_format = '$COLOR$BOLD%(asctime)s.%(msecs)03d <%(levelname)-4s><%(name)s:%(process)d:' \
                        '%(threadName)s>$RESET$COLOR<%(filename)s:%(lineno)d>%(message)s'
    log_file_format = '%(asctime)s.%(msecs)03d <%(levelname)-4s><%(name)s:%(process)d:%(threadName)s>' \
                      '<%(filename)s:%(lineno)d>%(message)s'

    def __init__(
            self,
            application: str,
            filename: str = None,
            log_path: str = "./logs",
            level: str = 'INFO',
            max_bytes: int = 100,
            backup: int = 10
    ):
        """
        :param application: application name, required param.
        :param filename: log file name. When it is None, nothing will be written to the log file.
        :param log_path: log file path, Default is "./logs".
                        When filename is not None and it does not exist, will automatically create it.
        :param level: log level. Default is INFO.
        :param max_bytes: log file size . Default is 100MB (1024 * 1024 * 100)
        :param backup: number of backup. Default is 10.
        """
        super(Logger, self).__init__(application, level=getattr(logging, level.upper(), logging.INFO))

        if self.handlers:
            return

        formatter = ColoredFormatter(self.log_stderr_format, datefmt="%F %T")
        streamer_handler = StreamHandler()
        streamer_handler.setFormatter(formatter)
        self.addHandler(streamer_handler)

        if filename:
            os.makedirs(log_path, exist_ok=True)
            filename = os.path.join(log_path, filename)
            file_formatter = logging.Formatter(fmt=self.log_file_format, datefmt="%F %T")
            file_handler = RotatingFileHandler(
                filename=filename,
                maxBytes=max_bytes * 1024 * 1024,
                backupCount=backup
            )
            file_handler.setFormatter(file_formatter)
            self.addHandler(file_handler)


if __name__ == '__main__':
    logger = Logger(application='demo', filename='demo.log', level="DEBUG")
    logger.info("111111111111111111111111")
    logger.error("2222222222222222222222222222")
    logger.warning("333333333333333333333333333")
    logger.debug("4444444444444444444444444444444")
    logger.critical("55555555555555555555555555555555")