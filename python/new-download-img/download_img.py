import urllib.request
import pymysql.cursors
import datetime
import time
import os


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2018-06-28

# update time: 2018-07-25


class DownloadFaceImage:

    strLogDir = "logs/"
    strImgDirName = "img/"
    strSqlFileName = "getFaceImage.sql"

    def __init__(self):

        self.runDo()


    def runDo(self):

        self.logUtilObj = LogUtil(self.strLogDir)
        self.doSearchObj = DoSearch(self.logUtilObj)
        self.downloadUtil = DownloadUtil(self.logUtilObj)
        runTime = RunTime()

        self.logUtilObj.writerLog("=========执行下载--" + runTime.getDateTime() + "=========")
        self.logUtilObj.writerLog("读取查询sql....")

        strGetMsgSql = self.logUtilObj.readFileContent(self.strSqlFileName)

        self.logUtilObj.writerLog("读取到的sql内容为: " + strGetMsgSql)
        lisrDictResultObj = self.doSearchObj.doSearchBySql(strGetMsgSql)

        self.logUtilObj.writerLog("共查找到" + str(len(lisrDictResultObj)) + "条数据")
        self.logUtilObj.writerLog("例第一条数据: " + str(lisrDictResultObj[0]))
        self.logUtilObj.writerLog("准备下载图片")


        intIndex = 1
        for listDictItem in lisrDictResultObj:

            strNextDirName = str(listDictItem.get('faceId'))
            strSavPathName = self.strImgDirName + strNextDirName

            strFirstImageUrl = str(listDictItem.get('picUrl_1'))

            if(strFirstImageUrl != ''):

                self.logUtilObj.writerLog("正在下载第 " + str(intIndex) + ' - 1张图片')
                strFirstImageName = strNextDirName + '-1.jpg'
                self.downloadUtil.downloadImg(strFirstImageUrl, strSavPathName, strFirstImageName)
            else:
                self.logUtilObj.writerLog('picUrl_1为空, 不执行下载')

            strTwoImageUrl = str(listDictItem.get('picUrl_2'))

            if(strTwoImageUrl != ''):

                self.logUtilObj.writerLog("正在下载第 " + str(intIndex) + ' - 2张图片')
                strTwoImageName = strNextDirName + '-2.jpg'
                self.downloadUtil.downloadImg(strTwoImageUrl, strSavPathName, strTwoImageName)
            else:
                self.logUtilObj.writerLog('picUrl_2为空, 不执行下载')

            intIndex += 1

        self.logUtilObj.writerLog("=========下载完成--" + runTime.getDateTime() + "=========")


class DownloadUtil:

    # 下载类

    def __init__(self, logUtilObj):

        self.logUtilObj = logUtilObj

    def downloadImg(self, strImgUrl, strSavePath, strImageName):

        # 下载并保存图片
        # strImgUrl: 图片url
        # strSavePath: 图片存放路径名和图片名字

        # if strImgUrl == 'no':
        #     self.logUtilObj.writerLog(strSavePath + strImgUrl + "---->未图片链接---->未下载")
        # elif strImgUrl == 'qn-no':
        #     self.logUtilObj.writerLog(strSavePath + strImgUrl + "---->未图片链接---->不下载")
        # else:

        header = {
            'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/'
                           '604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),
            'Cookie': 'connect.sid=s%3AfUMqGRS0y0ZaEkeLIwAtlVOD2lfQDpmd.hm%2FXSippPDk2g91PkOG1eXpn17ceblg8BdUigVBe6KQ'
        }

        intIndexDownTime = time.time()
        strOldPath = os.getcwd()

        self.logUtilObj.checkAndCreateDir(strSavePath)

        try:

            os.chdir(strSavePath)
            requestObj = urllib.request.Request(strImgUrl, None, header)
            responseObj = urllib.request.urlopen(requestObj)
            imgObj = responseObj.read()

            if('code' in str(imgObj)):
                self.logUtilObj.writerLog(strImageName + "未找到图片,未下载")
            else:
                with open(strImageName, 'wb') as fileObj:
                    fileObj.write(imgObj)

                os.chdir(strOldPath)
        except:
            os.chdir(strOldPath)
            self.logUtilObj.writerLog(strImageName + "请求出错.未下载")
        os.chdir(strOldPath)
        self.logUtilObj.writerLog(strImageName + "---->下载完成---" + str(round((time.time() - intIndexDownTime), 4)) + "s")


class DoSearch:

    #作为搜索查询的类

    def __init__(self, logUtilObj):

        self.logUtilObj = logUtilObj
        self.doMySql = DoMySql(self.logUtilObj)

    def doSearchBySql(self, strSearchSql):

        # 执行sql语句,这里用来做查找,这里每查询一次都回关闭连接
        # strSql: 要执行的sql语句
        # 返回一个list集合的结果

        listResult = []

        intIndexDownTime = time.time()

        connectionObj = self.doMySql.connectionMySQL()
        if (connectionObj is None):
            self.logUtilObj.writerLog("数据库连接失败")
        else:
            self.logUtilObj.writerLog("数据库已连接")
            pass

            try:
                with connectionObj.cursor() as cursor:

                    cursor.execute(strSearchSql)
                    listResult = cursor.fetchall()


                    # listResult = [{'index': 'no'}]
            except:
                self.logUtilObj.writerLog(strSearchSql + "查询时出错")

            finally:
                connectionObj.close()
                self.logUtilObj.writerLog("查询连接已关闭")

        if (len(listResult) == 0):
            self.logUtilObj.writerLog(strSearchSql + "未查找到数据")

        self.logUtilObj.writerLog("本次查询耗时: " + str(round((time.time() - intIndexDownTime), 4)) + "s")

        return listResult

    def doSearchMoreSql(self, strSql, connectionObj):

        # 这个方法同样用来查询数据库，但不同于上面的方法
        # 这个方法需要传入连接对象，并在外界控制连接的中断
        # 返回一个list结果

        listResult = []

        try:
            with connectionObj.cursor() as cursor:
                cursor.execute(strSql)
                listResult = cursor.fetchall()

            if (len(listResult) == 0):
                self.logUtilObj.writerLog(strSql + "未查找到数据")
                # listResult = [{'index': 'no'}]
        except:
            self.logUtilObj.writerLog("查询时出错")

        return listResult


class DoMySql:
    # 连接数据库

    strHost = '10.9.115.174'
    strPort = 3306
    strUser = 'haotuoguan'
    strPasswd = 'haotuoguan123456'
    strDatabase = 'haotuoguan'

    def __init__(self, logUtilObj):
        # 初始化对象
        self.logUtilObj = logUtilObj

    def connectionMySQL(self):

        # 连接数据库
        # 返回一个连接
        connection = None
        try:
            connection = pymysql.connect(host=self.strHost, port=self.strPort, user=self.strUser,
                                         passwd=self.strPasswd, db=self.strDatabase,
                                         charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
        except:
            self.logUtilObj.writerLog("连接数据库出错")

        if connection is None:
            self.logUtilObj.writerLog("数据库连接失败")
        else:
            # self.logUtilObj.writerLog("数据库连接成功")
            pass

        return connection


class LogUtil:



    def __init__(self, strLogDir):

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
            with open(self.strLogFileName, 'w', encoding='utf-8') as fileObj:
                fileObj.write(self.getDateTimeForLog() + strContent)
        print(self.getDateTimeForLog() + strContent)

    def checkAndCreateDir(self, strDirName):

        if(not (os.path.exists(strDirName))):
            os.makedirs(strDirName)
            self.writerLog(strDirName + "文件夹不存在,已自动创建")


    def readFileContent(self, inputFileName):

        # 读取普通文件内容并返回
        # 每次只读取1000字节

        strFileContent = ''

        with open(inputFileName, 'r', encoding='utf-8') as fileObj:

            while fileObj.readable():
                strFileContentItem = fileObj.read(1000)
                if (strFileContentItem != ''):
                    strFileContent += strFileContentItem
                else:
                    break

        return strFileContent


    def getDateTimeForLog(self):

        strTime = str(self.getTime("%Y-%m-%d %H:%M:%S"))
        return '[' + strTime + ']: '


    def getTime(self, strFormat):

        # 按照格式获取时间

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime


class RunTime:

    def getDateTime(self):
        nowTime = time.localtime()
        strFormatTime = time.strftime("%Y-%m-%d %H:%M:%S", nowTime)
        return strFormatTime

    def getPastDataDay(self, intDayNum):
        # 根据天数，来获取过去距离今天intDayNum天的日期
        # intDayNum: int类型, 表示天数
        # 返回的是一个date对象类型的日期,格式是"%Y-%m-%d"

        strToday = datetime.date.today()
        # strToday的日期格式就是"%Y-%m-%d"
        strOtherday = strToday - datetime.timedelta(days=intDayNum)

        return strOtherday

    def getFutureDataDay(self, intDayNum):
        # 根据天数，来获取未来距离今天intDayNum天的日期
        # intDayNum: int类型, 表示天数
        # 返回的是一个date对象类型的日期,格式是"%Y-%m-%d"

        strToday = datetime.date.today()
        # strToday的日期格式就是"%Y-%m-%d"
        strOtherday = strToday + datetime.timedelta(days=intDayNum)

        return strOtherday

    def getTimeStamp(self, strDate, strFormatDate):
        # 根据日期，获取时间戳
        # strDate: 字符串类型的日期
        # strFormatDate: 与strDate先对应的日期格式，例如"%Y-%m-%d"
        # 返回一个int类型的时间戳

        timeArray = time.strptime(strDate, strFormatDate)
        timeStamp = time.mktime(timeArray)

        return int(timeStamp)

    def getTodayStamp(self):
        # 获取今天的时间戳
        # 返回的是一个int类型的时间戳,日期格式是"%Y-%m-%d"

        strToday = datetime.date.today()
        timeArray = time.strptime(str(strToday), "%Y-%m-%d")
        timeStamp = time.mktime(timeArray)

        return int(timeStamp)


    def getDataByStamp(self, intStamp):
        # 根据时间戳来返回时间
        # data格式

        localData = time.localtime(intStamp/1000)
        dataByStamp = time.strftime("%Y-%m-%d-%H:%M:%S", localData)
        return dataByStamp


    def getDataByStampNew(self, intStamp):
        # 根据时间戳来返回时间
        # data格式

        localData = time.localtime(intStamp/1000)
        dataByStamp = time.strftime("%Y%m%d%H%M%S", localData)
        return dataByStamp


    def getDateTimeForLog(self):

        strTime = str(self.getTime("%Y-%m-%d %H:%M:%S"))
        return '[' + strTime + ']: '


    def getTime(self, strFormat):

        # 按照格式获取时间

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime




downloadFaceImageObj = DownloadFaceImage()