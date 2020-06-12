#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from threading import Thread
from utils.fileutils import getMd5
from services.config import XmlConfigInfo
from utils.log import Log

from abc import abstractmethod
from time import sleep

"""
MonitorParentProcess用于 热加载、热刷新 配置文件

而MonitorChildControllableThread线程类则是能够被MonitorParentProcess线程指挥的线程。
"""


class MonitorChildControllableThread(Thread):
    """
    Thread的子类。

    MonitorChildControllableThread抽象线程类，通过提供goon()方法和suspend()方法，修改shouldRunning属性。
    来使其子类线程shouldRunning属性变化，从而使子类线程进入等候循环。子类线程再次进入循环时需要重新获取配置文件信息。
    """

    def __init__(self):
        Thread.__init__(self)
        self.configFilePath = XmlConfigInfo.configFilePath

    configFilePath = XmlConfigInfo.configFilePath

    shouldRunning = False

    def goon(self):
        self.shouldRunning = True

    def suspend(self):
        self.shouldRunning = False

    @abstractmethod
    def run(self):
        pass


class MonitorParentProcess(Thread):
    """
    MonitorParentProcess用于 热加载、热刷新 配置文件
    """

    def __init__(self):
        # 必须在此处导包，否则会引发循环依赖问题，抛出ImportError异常
        from services.alarmclock import AlarmClockService
        from services.reminder import ReminderService
        from services.birthday import BirthdayService

        Thread.__init__(self)
        self.name = "configFlushMonitorService"

        # 初始化服务
        alarmClockService = AlarmClockService()
        reminderService = ReminderService()
        birthdayService = BirthdayService()

        self.services = [
            alarmClockService,
            reminderService,
            birthdayService
        ]

        self.protectionTime = max(
            alarmClockService.listeningFlushTime,
            reminderService.listeningFlushTime,
            birthdayService.listeningFlushTime
        ) + 1.5

    configFilePath = XmlConfigInfo.configFilePath

    # 服务列表（__init__方法初始化）
    services = []

    # 检查配置文件更新间隔时间
    flushTime = 0.5

    # 等待 子线程进入等候重载状态 的保险等候时间（__init__方法初始化）
    #     避免重载配置过快，导致子线程执行时 还没进入下一轮判断循环 shouldRunning的值就变更了两次
    #     (此时子线程不会退出循环进行重载) ，因而导致没有重载配置文件。
    protectionTime = 0

    def run(self):
        Log.info("服务启动。")
        XmlConfigInfo.init()
        oldMd5 = getMd5(self.configFilePath)
        for s in self.services:
            s.start()
        while True:
            newMd5 = getMd5(self.configFilePath)
            if newMd5 != oldMd5:  # 检测到配置文件更新，则暂停所有服务，刷新配置，然后重启服务
                oldMd5 = newMd5
                for s in self.services:
                    s.suspend()
                XmlConfigInfo.parse()
                sleep(self.protectionTime)
                for s in self.services:
                    s.goon()
                Log.info("配置文件刷新完成。")
            sleep(self.flushTime)
