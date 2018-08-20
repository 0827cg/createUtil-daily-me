#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2018-07-24


import os
import datetime
import time


class CopyRename:

    strLogDir = "logs/"
    strSaveImageDir = "img"
    intMaxDirNum = 1
    intMaxDirItemNum = 50
    intFileName = 0

    def __init__(self):

        self.logUtil = LogUtil(self.strLogDir)


    def traverDir(self, strDir):

        # 遍历文件夹
        # 遍历后, 取出intMaxDirNum个文件夹, 新产生的文件夹以1~intMaxDirNum来命名
        # 并将单个文件夹中的图片取出intMaxDirItemNum张, 新复制产生的文件以1~intMaxDirItemNum来命名
        # strDir: 需要遍历复制的文件夹父目录路径

        intNewDirName = 0

        for strRootDirName, listDirName, listFileName in os.walk(strDir):

            listPathItem = strRootDirName.split(os.sep)

            # self.logUtil.writerLog(str(listPathItem))
            # self.logUtil.writerLog(strRootDirName)
            # self.logUtil.writerLog(str(listFileName))
            # self.logUtil.writerLog(str(listDirName))

            if(len(listFileName) != 0):

                intNewDirName += 1

            intPicNum = 0

            if intNewDirName <= self.intMaxDirNum:

                for strFileName in listFileName:

                    if(intPicNum < self.intMaxDirItemNum):

                        strDiff = self.logUtil.getTimeForLog()

                        strFilePathName = strRootDirName + os.sep + strFileName

                        strSaveFilePath = self.strSaveImageDir + '-' + strDiff + os.sep + str(intNewDirName)

                        strNewFileName = str(intPicNum +1) + '.jpg'

                        self.copyFile(strFilePathName, strSaveFilePath, strNewFileName)

                        self.logUtil.writerLog(('-->' + str(intNewDirName) + '--' + str(intPicNum + 1) + '已完成拷贝'))

                        # self.logUtil.writerLog(strRootDirName + os.sep + strFileName)
                        # self.logUtil.writerLog(((len(listPathItem) * '---') + strFileName))

                    else:
                        break

                    intPicNum += 1
            else:
                self.logUtil.writerLog('dir num已达到最大值')
                self.logUtil.writerLog('程序将退出')
                break


    def newTraverDir(self, strDir, intRunNum, intTotalFileNum):

        # 这里的方法有bug, copyRename-test-1.py中的方法有效

        intIndexTime = time.time()
        intNeedRun = int((self.intMaxDirNum * self.intMaxDirItemNum) / intTotalFileNum) + 1
        intHasCopyNumEvery = 0

        strForDiff = self.logUtil.getTimeForLog()

        if intRunNum <= intNeedRun:

            # if (intHasCopyNumEvery <= intTotalFileNum):

                for strRootDirName, listDirName, listFileName in os.walk(strDir):

                        for strFileName in listFileName:

                            if self.intFileName < (self.intMaxDirNum * self.intMaxDirItemNum):

                                self.intFileName += 1
                                intHasCopyNumEvery += 1

                                if (intHasCopyNumEvery <= intTotalFileNum):

                                    strFilePath = strRootDirName + os.sep + strFileName
                                    strSaveFilePath = self.strSaveImageDir + '-' + strForDiff + os.sep
                                    strFileName = str(self.intFileName) + os.path.splitext(strFileName)[1]

                                    self.logUtil.writerLog('-->执行第' + str(intRunNum) + '次拷贝, intHasCopyNumEvery=' + str(intHasCopyNumEvery))
                                    self.copyFile(strFilePath, strSaveFilePath, strFileName)
                                    self.logUtil.writerLog(str(intRunNum) + '-' + str(intHasCopyNumEvery) + '-->' + strSaveFilePath + strFileName)
                                else:
                                    self.newTraverDir(strDir, intRunNum + 1, intTotalFileNum)

                            else:
                                self.logUtil.writerLog('已拷贝的图片总数已达到要求, self.intFileName = ' + str(self.intFileName))
                                break;
            # else:
            #     self.newTraverDir(strDir, intRunNum + 1, intTotalFileNum)

        else:
            self.logUtil.writerLog('重复拷贝次数intRunNum已达超过估计值, intRunNum = ' + str(intRunNum))
            self.logUtil.writerLog('程序将退出')



    def doNewTraverDir(self, strDir, intRunNum, intTotalFileNum):

        intIndexTime = time.time()

        intNeedRun = int((self.intMaxDirNum * self.intMaxDirItemNum) / intTotalFileNum) + 1

        self.logUtil.writerLog('现有总的文件个数: ' + str(intTotalFileNum))
        self.logUtil.writerLog('需要得到文件个数: ' + str(self.intMaxDirNum * self.intMaxDirItemNum))
        self.logUtil.writerLog('预计重复执行次数: ' + str(intNeedRun))

        self.newTraverDir(strDir, intRunNum, intTotalFileNum)

        self.logUtil.writerLog("总耗时: " + str(round((time.time() - intIndexTime), 4)) + "s")





    def getTotaoFileNum(self, strDir):

        # 获取文件夹内所有的.*文件个数

        intFileNum = 0

        for strRootDirName, listDirName, listFileName in os.walk(strDir):
            for strFileName in listFileName:
                intFileNum += 1

        return intFileNum







    def copyFile(self, strFilePath, strSaveFilePath, strFileName):

        # 复制文件
        # strFilePath: 需要复制的文件存放路径(全路径)
        # strSaveFilePath: 复制到的存在位置
        # strFileName: 保存的文件名

        # print('strFilePath: ' + strFilePath)
        # print('strSaveFilePath: ' + strSaveFilePath)
        # print('strFileName: ' + strFileName)
        # print('corrent path: ' +  os.getcwd())

        fileObj = open(strFilePath, 'rb')

        fileObjContent = fileObj.read()

        if not os.path.exists(strSaveFilePath):
            os.makedirs(strSaveFilePath)
            self.logUtil.writerLog('已创建目录: ' + strSaveFilePath)

        newFileObj = open(strSaveFilePath + os.sep + strFileName, 'wb')
        newFileObj.write(fileObjContent)

        fileObj.close()
        newFileObj.close()

        self.logUtil.writerLog((strFilePath + '-->: ' + strSaveFilePath + os.sep + strFileName))




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


    def getTimeForLog(self):

        strTime = str(self.getTime("%Y%m%d%H"))
        return strTime


    def getTime(self, strFormat):

        # 按照格式获取时间

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime


strDir = 'D:\Test\download_img\img-total-test'
copyRenameObj = CopyRename()
intTotalFileNum = copyRenameObj.getTotaoFileNum(strDir)
copyRenameObj.doNewTraverDir(strDir, 1, intTotalFileNum)
