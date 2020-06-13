#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string


def loopReplace(targetStr, old, new, loopCountLimit=10000):
    try:
        targetStr = str(targetStr)
    except ValueError:
        raise ValueError("stringutils.loopReplace()抛出异常：" + targetStr + "无法转换为字符串")
    try:
        old = str(old)
    except ValueError:
        raise ValueError("stringutils.loopReplace()抛出异常：" + old + "无法转换为字符串")
    try:
        new = str(new)
    except ValueError:
        raise ValueError("stringutils.loopReplace()抛出异常：" + new + "无法转换为字符串")
    i = 0
    while old in targetStr:
        targetStr = targetStr.replace(old, new)
        i += 1
        if i > loopCountLimit:
            raise RuntimeError(
                "stringutils.loopReplace()抛出异常：循环次数超出限制，请检查代码逻辑：target=" + targetStr + ",old=" + old + ",new=" + new + "。")
    return targetStr
