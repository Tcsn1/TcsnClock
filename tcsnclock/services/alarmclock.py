#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from services.config import XmlConfigInfo
from utils.timeutils import getDefaultTimeStamp
import time
import services.monitor as monitor
from utils.message import Msg

"""
AlarmClockService是闹钟服务
"""


class AlarmClockService(monitor.MonitorChildControllableThread):
    def __init__(self):
        monitor.MonitorChildControllableThread.__init__(self)
        self.name = "alarmClockService"

    # 闹钟监听间隔时间
    listeningFlushTime = 0.5

    # 无配置(shouldRunning = False)时暂停周期
    suspendFlushTime = 3

    def run(self):
        self.shouldRunning = True
        while True:
            # if self.shouldRunning and XmlConfigInfo.AlarmClock.enable:
            while self.shouldRunning and XmlConfigInfo.AlarmClock.enable:
                # 执行业务代码
                nowTimeStruct = time.localtime(time.time())
                nowTimeStamp = time.time()
                for a in XmlConfigInfo.AlarmClock.alarmClocks:
                    clockTimeStamp = getDefaultTimeStamp(None, None, None, a[0][0], a[0][1], a[0][2])
                    if nowTimeStamp + self.listeningFlushTime / 2 >= clockTimeStamp > nowTimeStamp - self.listeningFlushTime / 2 \
                            and nowTimeStruct[6] + 1 in a[1]:
                        # 闹钟响起
                        Msg.alarmClockMessage(a)
                time.sleep(self.listeningFlushTime)
            # 等待配置文件重载完成
            time.sleep(self.suspendFlushTime)
