#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from xml.dom import minidom
from utils import timeutils
from os.path import isfile
from os.path import isdir
from os.path import exists
from os import makedirs
from utils.fileutils import createFile
from utils.fileutils import Path
from utils.log import Log

"""
    XmlConfigInfo为配置类，提供了生成配置文件模版、解析配置文件、获取配置信息等功能。
        有如下属性：
        configFilePath  配置文件路径

    XmlConfigInfo.AlarmClock内部配置类，有如下属性：
        enable  是否启用
        alarmClocks 闹钟信息列表

    XmlConfigInfo.Birthday内部配置类，有如下属性：
        enable  是否启用
        birthdaysPreRemind  提前天数
        birthdaysRemindTime 提醒时间
        birthdays   生日信息列表

    XmlConfigInfo.Reminder内部配置类，有如下属性：
        enable  是否启用
        reminders   事件提醒信息列表
"""


class XmlConfigInfo:

    def __new__(cls, *args, **kwargs):
        raise Exception("配置类XmlConfigInfo禁止被实例化")

    # configFilePath为配置文件路径
    configFilePath = Path.getProjectPath("data/config.xml")

    @classmethod
    def parse(cls, file=configFilePath):
        """
        该方法用于解析xml配置文件的内容到该类的属性中。
        :param file: 可以不指定，也可以指定为配置文件的路径
        """
        try:
            # 解析xml并获取根节点<config>
            doc = minidom.parse(file)
            root = doc.documentElement
            if root.nodeName != "config":
                raise XmlConfigurationFileFormatErrorException("<config>根节点不存在")
            # 解析<birthdays>标签
            cls.AlarmClock.parse(root)
            # 解析<birthdays>标签
            cls.Birthday.parse(root)
            # 解析<reminders>标签
            cls.Reminder.parse(root)
        except XmlConfigurationFileFormatErrorException:
            cls.AlarmClock.resetProperties()
            cls.Birthday.resetProperties()
            cls.Reminder.resetProperties()
            raise XmlConfigurationFileFormatErrorException("配置文件解析失败，请检查配置文件 " + cls.configFilePath)

    class AlarmClock:
        def __new__(cls, *args, **kwargs):
            raise Exception("配置类XmlConfigInfo.AlarmClock禁止被实例化")

        # enable属性用于表明是否存在<birthdays>标签
        # 即是否启用闹钟功能
        enable = False

        # alarmClocks列表数据格式：
        # [
        #   [  [时,分,秒]  ,  [星期列表]  ,  文本描述  ],
        #   ...
        # ]
        alarmClocks = []

        @classmethod
        def resetProperties(cls):
            cls.enable = False
            cls.alarmClocks = []

        @classmethod
        def parse(cls, xmlRoot):
            cls.resetProperties()
            # 解析<alarmclocks>标签
            alarmClocksTags = xmlRoot.getElementsByTagName("alarmclocks")
            if len(alarmClocksTags) == 0:
                cls.enable = False
                return
            cls.enable = True
            alarmClocksTags = alarmClocksTags[0]
            # 解析<alarmclocks>标签下的<alarmclock>标签
            alarmClockArray = alarmClocksTags.getElementsByTagName("alarmclock")
            result = []
            for a in alarmClockArray:
                # 获取配置信息
                timeString = a.getAttribute("time")
                weekString = a.getAttribute("week")
                text = a.childNodes[0].data
                # 检验时间合法性
                try:
                    timeList = timeutils.parseTimeStringToList(timeString)
                except timeutils.TimeFormatErrorException:
                    raise XmlConfigurationFileFormatErrorException(
                        "<alarmclock>节点 " + text + " time属性格式错误：" + timeString)
                # 检验星期合法性
                try:
                    weekList = timeutils.parseWeekStringToList(weekString)
                    if len(weekList) == 0:
                        weekList = [1, 2, 3, 4, 5, 6, 7]
                except timeutils.WeekFormatErrorException:
                    raise XmlConfigurationFileFormatErrorException(
                        "<alarmclock>节点 " + text + " week属性格式错误：" + weekString)
                # 将数据插入cls.alarmClocks
                result.append([timeList, weekList, text])
            result.sort(key=lambda x: x[0][0] * 24 + x[0][1] * 60 + x[0][2] * 60)  # 按照时间先后进行排序
            cls.alarmClocks = result
            #     # 获取配置信息
            #     timeString = b.getAttribute("date")
            #     text = b.childNodes[0].data
            #     # 检验日期合法性
            #     if timeString == "":
            #         raise XmlConfigurationFileFormatErrorException("<birthday>节点 " + text + " 未设置属性date=\"\"")
            #     try:
            #         date = timeutils.parseDateStringToList(timeString)
            #     except timeutils.DateFormatErrorException:
            #         raise XmlConfigurationFileFormatErrorException("<birthday>节点 " + text + " date属性格式错误：" + timeString)
            #     # 将数据插入cls.birthdays
            #     cls.birthdays.append([date, text])
            # cls.birthdays.sort(key=lambda x: x[0][1] * 31 + x[0][2])  # 按照日期先后进行排序

    class Birthday:

        def __new__(cls, *args, **kwargs):
            raise Exception("配置类XmlConfigInfo.Birthday禁止被实例化")

        # enable属性用于表明是否存在<birthdays>标签
        # 即是否启用生日提醒功能
        enable = False

        # preRemind属性所对应。
        # birthdaysPreRemind为提前提醒的天数，可以不设置
        # 如果设置了该属性，会在生日到来的前n天提醒，并且生日当天也会提醒
        birthdaysPreRemind = 0

        # remindTime属性所对应。
        # birthdaysRemindTime为生日提醒时间
        # 格式为：[时,分,秒]
        birthdaysRemindTime = []

        # birthdays列表数据格式：
        # [
        #   [  [(年 或 unknown),月,日]  ,  文本描述  ],
        #   ...
        # ]
        birthdays = []

        @classmethod
        def resetProperties(cls):
            # 重置属性
            cls.enable = False
            cls.birthdaysPreRemind = 0
            cls.birthdaysRemindTime = []
            cls.birthdays = []

        @classmethod
        def parse(cls, xmlRoot):
            cls.resetProperties()
            # 解析<birthdays>标签属性
            birthdaysTags = xmlRoot.getElementsByTagName("birthdays")
            if len(birthdaysTags) == 0:
                cls.enable = False
                return
            cls.enable = True
            birthdaysTags = birthdaysTags[0]
            # # 解析remindTime属性
            remindTime = birthdaysTags.getAttribute("remindTime")
            if remindTime == "":  # 属性不存在
                raise XmlConfigurationFileFormatErrorException("<birthdays>标签 未设置属性remindTime=\"\"")
            try:
                cls.birthdaysRemindTime = timeutils.parseTimeStringToList(remindTime)  # 检验时间格式合法性
            except timeutils.TimeFormatErrorException:
                raise XmlConfigurationFileFormatErrorException("<birthdays>标签 属性remindTime格式有误：" + remindTime)
            # # 解析preRemind属性
            preRemind = birthdaysTags.getAttribute("preRemind")
            if preRemind == "":  # 未设置属性
                cls.birthdaysPreRemind = 0
            else:
                try:
                    preDays = int(preRemind)
                    if preDays >= 0:
                        cls.birthdaysPreRemind = preDays
                    else:
                        raise XmlConfigurationFileFormatErrorException(
                            "<birthdays>标签 属性preRemind格式有误：" + preRemind + " (提前的天数)必须为正数")
                except ValueError:
                    raise XmlConfigurationFileFormatErrorException(
                        "<birthdays>标签 属性preRemind格式有误：" + preRemind + " 无法转成数字")
            # 解析<birthdays>标签下的<birthday>标签
            birthdayArray = birthdaysTags.getElementsByTagName('birthday')
            result = []
            for b in birthdayArray:
                # 获取配置信息
                timeString = b.getAttribute("date")
                text = b.childNodes[0].data
                # 检验日期合法性
                if timeString == "":
                    raise XmlConfigurationFileFormatErrorException("<birthday>节点 " + text + " 未设置属性date=\"\"")
                try:
                    date = timeutils.parseDateStringToList(timeString)
                except timeutils.DateFormatErrorException:
                    raise XmlConfigurationFileFormatErrorException("<birthday>节点 " + text + " date属性格式错误：" + timeString)
                # 将数据插入cls.birthdays
                result.append([date, text])
            result.sort(key=lambda x: x[0][1] * 31 + x[0][2])  # 按照日期先后进行排序
            cls.birthdays = result

    class Reminder:

        def __new__(cls, *args, **kwargs):
            raise Exception("配置类XmlConfigInfo.Reminder禁止被实例化")

        # enable属性用于表明是否存在<reminders>标签
        # 即是否启用事件提醒功能
        enable = False

        # reminders列表数据格式：
        # [
        #   [  时间毫秒值  ,  文本描述  ],
        #   ...
        # ]
        reminders = []

        @classmethod
        def resetProperties(cls):
            cls.enable = False
            cls.reminders = []

        @classmethod
        def parse(cls, xmlRoot):
            cls.resetProperties()
            # 解析<reminders>标签
            remindersTags = xmlRoot.getElementsByTagName("reminders")
            if len(remindersTags) == 0:
                cls.enable = False
                return
            cls.enable = True
            remindersTags = remindersTags[0]

            # 解析<reminders>标签下的<reminder>标签
            reminderArray = remindersTags.getElementsByTagName("reminder")
            result = []
            for r in reminderArray:
                text = r.childNodes[0].data
                timeString = r.getAttribute("time")
                if timeString == "":
                    raise XmlConfigurationFileFormatErrorException("<reminder>节点 " + text + " 未设置属性time=\"\"")
                try:
                    time = timeutils.parseDateTimeStringToTime(timeString)
                except timeutils.DateTimeFormatErrorException:
                    raise XmlConfigurationFileFormatErrorException("<reminder>节点 " + text + " time属性格式错误：" + time)
                result.append([time, text])
            result.sort(key=lambda t: t[0])
            cls.reminders = result

    @classmethod
    def init(cls):
        Log.info("配置文件路径：" + cls.configFilePath)
        createFile(cls.configFilePath, _configXmlTemplate())
        cls.parse()


class XmlConfigurationFileFormatErrorException(Exception):
    """
    解析xml配置文件时发生的格式错误异常。
    """

    def __init__(self, err=""):
        super().__init__("xml配置文件 " + XmlConfigInfo.configFilePath + " 格式错误：" + err)


def _configXmlTemplate():
    """
    :return:返回一个配置文件模版的字符串。
    """
    str = \
        u"""<?xml version="1.0" encoding="UTF-8" ?>
        <config>
            <!-- alarmclocks标签用于设置闹钟  -->
            <alarmclocks>
                <!--
                    time属性是闹钟时间
                    week属性代表星期x生效，可以不设置(默认每天都生效)
                    标签内是文本描述
                    示例如下：<alarmclock time="时:分" week="[星期x,星期x,...]">文本描述</alarmclock>
                -->
                <alarmclock time="8:30" week="[1,2,3,4,5]">上班</alarmclock>
                <alarmclock time="23:00">睡觉</alarmclock>
            </alarmclocks>
            
        
            <!-- reminders标签用于设置备忘录  -->
            <reminders>
                <!--
                    time属性是事件提醒时间
                    标签内是文本描述
                    示例如下：<reminder time="年.月.日 时:分:秒">文本描述</reminder>
                -->
                <reminder time="2019.11.14 19:19:19">1个小时后看电影</reminder>
                <reminder time="1977.7.7 7:7:7">七夕节给女朋友买礼物</reminder>
            </reminders>
        
            
            <!-- birthdays标签用于设置生日提醒  -->
            <!--
                remindTime属性：一天中提醒您的时间，设为12:00:00即会在12点提醒生日信息
                preRemind属性：提前提醒的时间。设置后会在 生日当天 和 x天前 提醒您，。可以不设置。
            -->
            <birthdays remindTime="12:00:00" preRemind="2">
                <!--
                    data属性用于指定日期，标签内是文本描述
                    示例如下：<birthday date="月.日">文字描述</birthday>
                -->
                <birthday date="11.11">小黑的生日</birthday>
                <birthday date="2000.10.10">小花的生日</birthday>
            </birthdays>
        </config>
        
        """
    return str
