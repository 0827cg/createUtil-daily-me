#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2018-08-23

import time


class DateOper:

    def getDayNum(self, strDate):

        # strDate: 日期字符串, 格式为%Y-%m-%d
        # %Y-%m-%d %H:%M:%S
        # 获取目前时间距离strDate过去的天数

        intPastTimeStamp = time.mktime(time.strptime(strDate, '%Y-%m-%d'))
        intTimeStampNum = time.time() - intPastTimeStamp
        intDayNum = int(round(intTimeStampNum / (24*3600), 0))

        return intDayNum


print(DateOper().getDayNum('2017-11-23'))