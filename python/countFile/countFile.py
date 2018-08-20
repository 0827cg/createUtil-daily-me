#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2018-07-24

import os
import datetime
import time

class CountFile:


    strLogDir = "logs/"

    def __init__(self):

        self.logUtil = LogUtil(self.strLogDir)


    def traverDir(self, strDir, intLevel):

        if intLevel == 1:
            print(strDir)

        listFile = os.listdir(strDir)

        for listFileItem in listFile:
            strPath = os.path.join(strDir, listFileItem)
            self.logUtil.writerLog(((intLevel * '---'),listFileItem))
            if os.path.isdir(strPath):
                self.traverDir(strPath, (intLevel + 1))

    def newTraverDir(self, strDir):


        self.logUtil.writerLog("====================")

        intIndexTime = time.time()

        intTotalFileNum = 0
        intTotalDirNum = 0

        for strRootDirNamee, listDir, listFile in os.walk(strDir):

            listPathItem = strRootDirNamee.split(os.sep)

            self.logUtil.writerLog(os.sep)

            self.logUtil.writerLog(str(listPathItem))
            self.logUtil.writerLog(strRootDirNamee)
            self.logUtil.writerLog(str(listFile))
            self.logUtil.writerLog(str(listDir))

            intTotalFileNum += len(listFile)
            intTotalDirNum += len(listDir)

            self.logUtil.writerLog(((len(listPathItem) - 1) * '---' + os.path.basename(strRootDirNamee)))
            for file in listFile:
                self.logUtil.writerLog(((len(listPathItem) * '---') + file))

        self.logUtil.writerLog('total file num: ' + str(intTotalFileNum))
        self.logUtil.writerLog('total dir num: ' + str(intTotalDirNum))
        self.logUtil.writerLog("耗时: " + str(round((time.time() - intIndexTime), 4)) + "s")


class LogUtil:

    # 用来做日志记录

    def __init__(self, strLogDir):

        # strLogDir: 存放日志文件的文件夹路径(支持相对路径)
        # 日志文件的名字目前只以日期来命名

        self.strLogDir = strLogDir

        strToday = str(datetime.date.today())
        self.strLogFileName = self.strLogDir + strToday + ".log"

        self.checkAndCreateDir(self.strLogDir)


    def writerLog(self, strContent, whetherAdd=True):

        #写入文件
        # whetherAdd: 是否换行,默认换行

        if(whetherAdd & True):
            with open(self.strLogFileName, 'a', encoding='utf-8') as fileObj:
                fileObj.write(self.getDateTimeForLog() + strContent + '\n')
        else:
            with open(self.strLogFileName, 'a', encoding='utf-8') as fileObj:
                fileObj.write(self.getDateTimeForLog() + strContent)

        print(self.getDateTimeForLog() + strContent)


    def checkAndCreateDir(self, strDirName):

        if(not (os.path.exists(strDirName))):
            os.makedirs(strDirName)
            self.writerLog(strDirName + "文件夹不存在,已自动创建")
            self.writerLog("=================")


    def getDateTimeForLog(self):

        strTime = str(self.getTime("%Y-%m-%d %H:%M:%S"))
        return '[' + strTime + ']: '


    def getTime(self, strFormat):

        # 按照格式获取时间

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime


# CountFile().printDir('D:\Test\download_img\orgId-2370', 1)
CountFile().newTraverDir('D:\Test\do-count')



