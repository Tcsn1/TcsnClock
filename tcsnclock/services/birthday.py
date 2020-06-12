#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from services.config import XmlConfigInfo
import time
import services.monitor as monitor
from utils.timeutils import getDefaultTimeStamp
from utils.message import Msg

"""
BirthdayService是生日提醒服务
"""


class BirthdayService(monitor.MonitorChildControllableThread):
    def __init__(self):
        monitor.MonitorChildControllableThread.__init__(self)
        self.name = "birthdayService"

    # 监听状态刷新时间
    listeningFlushTime = 1

    # 无配置(shouldRunning = False)时暂停周期
    suspendFlushTime = 3

    def run(self):
        self.shouldRunning = True
        while True:
            while self.shouldRunning and XmlConfigInfo.Birthday.enable:
                # 载入配置
                birthdays = XmlConfigInfo.Birthday.birthdays.copy()
                preRemindDay = XmlConfigInfo.Birthday.birthdaysPreRemind
                remindTime = XmlConfigInfo.Birthday.birthdaysRemindTime
                # 监听
                while self.shouldRunning and XmlConfigInfo.Birthday.enable:
                    # 到了提醒时间，则检查今天是否有生日
                    if time.time() - self.listeningFlushTime / 2 <= \
                            getDefaultTimeStamp(None, None, None, remindTime[0], remindTime[1], remindTime[2]) \
                            <= time.time() + self.listeningFlushTime / 2 \
                            and self.shouldRunning and XmlConfigInfo.Birthday.enable:
                        todayTimeStruct = time.localtime(time.time())
                        preTimeStruct = time.localtime(time.time() - preRemindDay * 24 * 60 * 60)
                        for b in birthdays:
                            if b[0][1] == todayTimeStruct[1] and b[0][2] == todayTimeStruct[2]:
                                Msg.birthdayMessage(b, 0)
                            if b[0][1] == preTimeStruct[1] and b[0][2] == preTimeStruct[2]:
                                Msg.birthdayMessage(b, preRemindDay)
                    time.sleep(self.listeningFlushTime)

            time.sleep(self.suspendFlushTime)
