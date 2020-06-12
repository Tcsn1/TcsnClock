#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class MainService:
    def __new__(cls, *args, **kwargs):
        raise Exception("Main类禁止被实例化")

    @classmethod
    def app_path(cls):
        import sys
        from os.path import dirname

        """Returns the base application path."""
        if hasattr(sys, 'frozen'):
            # Handles PyInstaller
            return dirname(sys.executable)  # 使用pyinstaller打包后的exe目录
        return dirname(__file__)  # 没打包前的py目录

    @classmethod
    def init(cls):
        from utils.fileutils import Path
        # 初始化路径
        Path.getProjectPath(initPath=cls.app_path())
        # 初始化日志
        from utils.log import Log
        Log.initLogFile(Path.getProjectPath("data/log.txt"))
        Log.info("项目路径：" + Path.getProjectPath(initPath=cls.app_path()))
        # 初始化提示音
        from utils.message import Msg
        Msg.initDingWav(Path.getProjectPath("data/ding.wav"))
        # 项目初始化完成

    @classmethod
    def start(cls):
        cls.init()
        from services.monitor import MonitorParentProcess
        MonitorParentProcess().start()


