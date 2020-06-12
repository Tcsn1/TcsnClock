#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from services.config import XmlConfigInfo
import time
import services.monitor as monitor
from utils.message import Msg

"""
ReminderService是备忘录服务
"""


class ReminderService(monitor.MonitorChildControllableThread):
    def __init__(self):
        monitor.MonitorChildControllableThread.__init__(self)
        self.name = "reminderService"

    # 监听状态刷新间隔时间
    listeningFlushTime = 1

    # 无配置(shouldRunning = False)时暂停周期
    suspendFlushTime = 3

    def run(self):
        self.shouldRunning = True
        while True:
            if self.shouldRunning and XmlConfigInfo.Reminder.enable:
                nowTimeStamp = time.time()
                reminders = XmlConfigInfo.Reminder.reminders.copy()
                # 先清除掉过期的事件
                for r in reminders.copy():
                    if r[0] <= nowTimeStamp:
                        reminders.remove(r)
                # 持续监听事件发生
                while self.shouldRunning and XmlConfigInfo.Reminder.enable and len(reminders) != 0:
                    nowTimeStamp = time.time()
                    for r in reminders:
                        if r[0] <= nowTimeStamp:
                            Msg.reminderMessage(r)
                            reminders.remove(r)
                    time.sleep(self.listeningFlushTime)
            time.sleep(self.suspendFlushTime)
