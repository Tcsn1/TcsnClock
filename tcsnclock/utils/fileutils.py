#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from hashlib import md5
from os import sep

from os import remove
from base64 import decode

from utils.log import Log
from os import makedirs
from os.path import exists
from os.path import isdir
from os.path import isfile


def writeBase64BytesOutToFile(base64Bytes, path):
    try:
        createFile(Path.getProjectPath("data/tmp"), base64Bytes, flags="byte")
        decode(open(Path.getProjectPath("data/tmp"), "r"), open(path, "wb"))
        remove(Path.getProjectPath("data/tmp"))
    except Exception as e:
        Log.error("flieutils.writeBase64BytesOutToFile()抛出异常。" + str(e))
        raise e


def createFile(filePath, context=None, flags="text"):
    """
    创建目录下的文件。（如果不存在则会递归创建目录和文件）
    :param filePath: 请传入Path.getProjectPath()的路径值。
    :param context:创建文件后，要写入的文本或二进制数据。为None则不写入。如果文件已存在，则该值无效。
    :param flags:标注该文件是文本文件还是二进制文件。
    """
    if flags not in ["text", "byte"]:
        raise Exception("flieutils.createFile()方法参数错误：flags值 " + flags + " 无效")
    # 创建目录
    pathArray = filePath.split(sep)
    length = len(pathArray)
    dirPath = ""
    for i in range(length - 1):
        dirPath += pathArray[i] + sep
    if not (exists(dirPath) and isdir(dirPath)):
        makedirs(dirPath)
    # 判断文件是否存在
    fileExist = exists(filePath) and isfile(filePath)
    f = None
    try:
        if not fileExist:  # 文件不存在，创建文件
            if flags == "text":
                f = open(filePath, "w", encoding="utf-8")
            elif flags == "byte":
                f = open(filePath, 'wb')
            # 写入文件
            if context is not None:
                f.write(context)
        else:  # 文件存在，不作修改
            pass
    except Exception as e:
        Log.error("flieutils.createFile()抛出异常。" + str(e))
        raise e
    finally:
        if f is not None:
            f.close


def getMd5(file):
    m = md5()
    f = None
    try:
        f = open(file, 'rb')
        for line in f:
            m.update(line)
    except Exception as e:
        Log.error("flieutils.getMd5()抛出异常。" + str(e))
        raise e
    finally:
        if f is not None:
            f.close()
    return m.hexdigest()


class Path:
    def __new__(cls, *args, **kwargs):
        raise Exception("Path类禁止被实例化")

    __projectPath = None

    @classmethod
    def getProjectPath(cls, appendPath="", initPath=None):
        from threading import Lock
        from mainservice import MainService

        if cls.__projectPath is None:
            with Lock():
                if cls.__projectPath is None:
                    if initPath is None:
                        cls.__projectPath = MainService.app_path()
                    else:
                        cls.__projectPath = initPath
        return (cls.__projectPath.replace("\\", "/").rstrip("/")
                + sep + appendPath.replace("\\", "/").lstrip("/")
                ).replace("/", sep)
