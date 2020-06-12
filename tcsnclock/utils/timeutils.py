#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time


class DateFormatErrorException(Exception):
    def __init__(self, err=""):
        super().__init__("timeutils:日期格式错误：" + err)


class TimeFormatErrorException(Exception):
    def __init__(self, err=""):
        super().__init__("timeutils:时间格式错误：" + err)


class DateTimeFormatErrorException(Exception):
    def __init__(self, err=""):
        super().__init__("timeutils:日期时间格式错误：" + err)


class WeekFormatErrorException(Exception):
    def __init__(self, err=""):
        super().__init__("timeutils:星期格式错误：" + err)


def exceedNow(dateTimeFormatString):
    """
    使用该方法返回 当前时间 减去 格式化时间 的差值（单位:秒）
    :param dateTimeFormatString: 输入"年.月.日 时:分:秒" 格式的时间
    :return: 返回相差的毫秒值
    """
    return time.time() - parseDateTimeStringToTime(dateTimeFormatString)


def parseDateTimeStringToTime(dateTimeFormatString):
    try:
        return time.mktime(time.strptime(dateTimeFormatString.replace("：", ":"), "%Y.%m.%d %H:%M:%S"))
    except ValueError:
        raise DateTimeFormatErrorException(dateTimeFormatString + "格式无效")


def parseDateStringToList(dateFormatString):
    """
    传入 "年.月.日" 或 "月.日" 字符串。
    该方法在dateFormatString格式不正确时，会抛出DateFormatErrorException异常，请方法调用者自行except
    如果格式正确，将会返回[year,month,day]列表

    :param dateFormatString: 传入 "年.月.日" 或 "月.日" 字符串
    :return:返回[year,month,day]列表
    """
    t = dateFormatString.replace('-', '.').split(".")
    try:
        if len(t) == 3:
            year = int(t[0])
            month = int(t[1])
            day = int(t[2])
        elif len(t) == 2:
            year = "unknown"
            month = int(t[0])
            day = int(t[1])
        else:
            raise DateFormatErrorException("日期格式错误：请输入\"年.月.日\"或\"月.日\"")
    except ValueError:
        raise DateFormatErrorException("日期格式错误：在 " + dateFormatString + " 中出现了非数字字符")
    if not dateListIsLegal([year, month, day]):
        raise DateFormatErrorException("日期格式错误：" + str(year) + "年" + str(month) + "月" + str(day) + "日 不存在")
    return [year, month, day]


def dateListIsLegal(listOfYearMonthDay):
    """
    传入 [年,月,日] 列表，判断是否合法。也可以传入['unknown',月,日]列表，将会默认为0年（闰年）。

    :param listOfYearMonthDay: [年,月,日] 列表  或  ['unknown',月,日]列表
    :return: 如果合法，返回True，否则返回False
    """
    dayInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if len(listOfYearMonthDay) != 3:
        return False
    try:
        if listOfYearMonthDay[0] == "unknown":
            year = 0
        else:
            year = int(listOfYearMonthDay[0])
        month = int(listOfYearMonthDay[1])
        day = int(listOfYearMonthDay[2])
    except ValueError:
        return False
    if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
        dayInMonth[1] += 1
    if 12 >= month > 0 and 0 < day <= dayInMonth[month - 1]:
        return True
    else:
        return False


def parseTimeStringToList(timeFormatString):
    """
    传入一个 "时:分:秒" 或 "时:分" 或 "时" 的字符串
    该方法在格式不正确时，会抛出TimeFormatErrorException异常，请方法调用者自行except
    如果格式正确，将会返回[hour,minute,second]列表

    :param timeFormatString: "时:分:秒" 或 "时:分" 或 "时" 的字符串
    :return: 返回[hour,minute,second]列表
    """
    t = timeFormatString.replace("：", ":").split(':')
    hour = 0
    minute = 0
    second = 0
    try:
        if len(t) == 1:
            hour = int(t[0])
        elif len(t) == 2:
            hour = int(t[0])
            minute = int(t[1])
        elif len(t) == 3:
            hour = int(t[0])
            minute = int(t[1])
            second = int(t[2])
        else:
            raise TimeFormatErrorException("时间格式错误：请输入\"时:分:秒\"或\"时:分\"或\"时\"")
    except ValueError:
        raise TimeFormatErrorException("时间格式错误：在 " + timeFormatString + "中存在无法转换为数字的字符")
    if not timeListIsLegal([hour, minute, second]):
        raise TimeFormatErrorException("时间格式错误：时间 " + str(hour) + "时" + str(minute) + "分" + str(second) + "秒 不存在")
    return [hour, minute, second]


def parseTimeStringToList2(timeFormatString):
    """
    传入一个 "分:秒" 的字符串
    该方法在格式不正确时，会抛出TimeFormatErrorException异常，请方法调用者自行except
    如果格式正确，将会返回[minute,second]列表

    :param timeFormatString: "分:秒" 的字符串
    :return: 返回[minute,second]列表
    """
    t = timeFormatString.replace("：", ":").split(':')
    minute = 0
    second = 0
    try:
        if len(t) == 2:
            minute = int(t[0])
            second = int(t[1])
        else:
            raise TimeFormatErrorException("时间格式错误：请输入\"分:秒\"")
    except ValueError:
        raise TimeFormatErrorException("时间格式错误：在 " + timeFormatString + "中存在无法转换为数字的字符")
    if not timeListIsLegal([0, minute, second]):
        raise TimeFormatErrorException("时间格式错误：时间 " + str(minute) + "分" + str(second) + "秒 不存在")
    return [minute, second]


def timeListIsLegal(listOfHourMinuteSecond):
    """
    传入[时,分,秒]列表，判断格式是否合法
    :param listOfHourMinuteSecond:[时,分,秒]列表
    :return:格式正确返回True，否则返回False
    """
    if len(listOfHourMinuteSecond) != 3:
        return False
    try:
        hour = int(listOfHourMinuteSecond[0])
        minute = int(listOfHourMinuteSecond[1])
        second = int(listOfHourMinuteSecond[2])
    except ValueError:
        return False
    if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
        return True
    else:
        return False


def parseWeekStringToList(weekFormatString):
    """
    解析 "[1,2,3,6,7]" 此类的字符串为数组
    :param weekFormatString:  "[1,2,3,6,7]" 或 "1,2,3,6,7"  这类字符串
    :return: 返回 [1,2,3,6,7]
    """
    weeks = weekFormatString.replace("[", "").replace("]", "").replace("；", ";") \
        .replace(";", ",").replace(".", ",").replace("，", ",").split(",")
    result = []
    try:
        for w in weeks:
            if w.replace(" ", "").replace("\t", "") == "":
                continue
            i = int(w)
            if i < 1 or i > 7:
                raise WeekFormatErrorException("星期格式错误：" + weeks + "中存在 >7或<1的数字 " + i + " ，请检查星期格式")
            result.append(i)
    except ValueError:
        raise WeekFormatErrorException("星期格式错误：" + weeks + "中存在无法转换为数字的字符 " + w + " ，请检查星期格式")
    return result


def getDefaultTimeStamp(year, month, day, hour, minute, second):
    """
    year, month, day, hour, minute, second 六个参数，如果传入None，则会使用此时的值。
    再根据这六个值，获取代表的时间戳
    :return:
    """
    now = time.localtime(time.time())
    if year is None:
        year = now[0]
    if month is None:
        month = now[1]
    if day is None:
        day = now[2]
    if hour is None:
        hour = now[3]
    if minute is None:
        minute = now[4]
    if second is None:
        second = now[5]
    return parseDateTimeStringToTime(
        str(year) + "." + str(month) + "." + str(day) + " "
        + str(hour) + ":" + str(minute) + ":" + str(second))


def getNowTimeString():
    return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))
