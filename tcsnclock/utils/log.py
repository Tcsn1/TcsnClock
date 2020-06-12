#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from utils.timeutils import getNowTimeString as nowTime

"""
Log日志类
"""


class Log:
    def __init__(self):
        raise Exception("Log日志类禁止被实例化")

    _logFilePath = None
    _useLogFile = False
    _outputStream = None

    @classmethod
    def initLogFile(cls, path=None):
        from utils.fileutils import createFile
        """
        :param path: 传入配置文件路径，如果为None。则不使用配置文件
        """
        if path is None:
            cls._useLogFile = False
            cls._logFilePath = None
        else:
            try:
                createFile(path)
                cls._logFilePath = path
                cls._useLogFile = True
                Log.info("设置日志文件成功，日志文件路径：" + cls._logFilePath)
            except Exception as e:
                cls._useLogFile = False
                cls._logFilePath = None
                Log.error("设置日志文件 " + path + " 失败")
                raise e

    @classmethod
    def _writeIntoLogFile(cls, text):
        if cls._useLogFile:
            print(text, file=open(cls._logFilePath, "a", encoding="utf-8"))

    @classmethod
    def info(cls, text):
        s = "[info] [" + nowTime() + "] " + text
        print(s)
        cls._writeIntoLogFile(s)

    @classmethod
    def error(cls, text):
        s = "[error] [" + nowTime() + "] " + text
        print(s)
        cls._writeIntoLogFile(s)

    @classmethod
    def message(cls, text):
        s = "[message] [" + nowTime() + "] " + text
        print(s)
        cls._writeIntoLogFile(s)
