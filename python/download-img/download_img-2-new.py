# -*- coding: utf-8 -*-

'''
根据org_id和shop_id(shop_id可为多),来获取学生签到时候抓拍下来的照片
步骤:
    1. 根据org_id和shop_id,从htg_sign_pic中获取卡号，卡号存在code字段中，code的值为 '卡号'+'_'+'时间戳(毫秒)'
    同时获取字段pic_url的值
    2. 根据获取的卡号从htg_users表中获取学生的姓名，字段为name

'''

# author: cg
# time: 2018-03-09
# update: 更新sql语句，in代替or,效率将提升一倍多
# update time: 2018-04-18

import urllib.request
import pymysql.cursors
import datetime
import time
import os


class DownloadImg:

    strLogDir = "logs/"
    # strSqlFileName = "getStudentSignMsg.sql"
    strSqlFileName = "getStudentMsgSql.sql"

    intOrgId = 1183
    intShopId_1 = 674
    intShopId_2 = 1447

    strImgDirName = "img" + str(intOrgId) + "/"

    strHtgUrl = 'http://file.haotuoguan.cn/download?shortid='
    strQnUrl = 'http://sign-pic.file.cdn.haotuoguan.cn/'

    def __init__(self):
        self.runDo()

    def runDo(self):
        self.runTime = RunTime()
        strDateTime = self.runTime.getDateTime()

        self.logUtil = LogUtil(self.strLogDir)
        self.logUtil.writerLog("==========" + strDateTime + "==========")
        print("==========" + strDateTime + "==========")

        doSearch = DoSearch(self.logUtil)
        downloadUtil = DownloadUtil(self.logUtil)

        # listResult = self.getCardAndUrl(doSearch)
        # listResultTotalMsg = self.getTotalMes(listResult, doSearch)

        strSql = self.logUtil.readFileContent(self.strSqlFileName)

        # strTotalSql = (strSql % (self.intOrgId, self.intShopId_1, self.intShopId_2))
        strTotalSql = (strSql % (self.intShopId_1, self.intShopId_2))

        # self.logUtil.writerLog("strTotalSql: " + strTotalSql)

        listResultTotalMsg = doSearch.doSearchBySql(strTotalSql)
        self.logUtil.writerLog("共查找到" + str(len(listResultTotalMsg)) + "条数据")
        self.logUtil.writerLog("例第一条数据: " + str(listResultTotalMsg[0]))
        print(str(listResultTotalMsg[0]))

        self.doBeginDown(listResultTotalMsg, downloadUtil)
        self.logUtil.writerLog("脚本本次执行完成")
        print("脚本本次执行完成")


    def getCardAndUrl(self, doSearchObj):

        # 通过org_id和两个shop_id来从表htg_sign_pic中获取code,pic_url,org_id和shop_id
        # 返回一个list结果,其元素为dict类型
        # pic_url可能为null，但其他三个就不可能为空

        # 废弃

        strSql = "SELECT code, pic_url, org_id, shop_id, sign_ids FROM htg_sign_pic " + \
                 " WHERE org_id = " + str(self.intOrgId) + " AND shop_id = " + str(self.intShopId_1) + \
                 " OR shop_id = " + str(self.intShopId_2)

        self.logUtil.writerLog("strSql: " + strSql)

        intIndexTime = time.time()
        self.logUtil.writerLog("--->准备从数据库中获取数据--getCardAndUrl()")
        listResult = doSearchObj.doSearchBySql(strSql)
        self.logUtil.writerLog("数据获取完成--getCardAndUrl().共查找到" + str(len(listResult)) + "条数据")
        self.logUtil.writerLog("第一条数据: " + str(listResult[0]))
        self.logUtil.writerLog("本次耗时: " + str(round(int(time.time() - intIndexTime), 4)) + "s")

        # 作为测试，只打印20条
        # for index in range(20):
        #     self.logUtil.writerLog(str(listResult[index]))


        return listResult

    def getTotalMes(self, listResult, doSearchObj):

        # 将code字段的值分开为card号和打卡时间戳
        # 根据对应的card号来获取名字
        # listResult: 初次从htg_sign_pic中查找到的list类型集合，其元素为dict类型，
        # 其dict中的key只有code, pic_url, org_id, shop_id, sign_ids
        # 现在此方法中，for循环会将card_num,append_time,student_id,name存放到listResult的dict中，添加key和value
        # 最后返回

        # connectionObjMore = doSearchObj.doMySql.connectionMySQL()

        # 废弃

        intIndexTwoTime = time.time()
        self.logUtil.writerLog("--->准备依次从数据库中获取全部所需数据--getTotalMes()")

        for index in range(len(listResult)):

            listSplitResult = str(listResult[index].get('code')).split('_')

            # 从code中截取card号和打卡时间戳，并加入listResult中的dict中
            listResult[index]['card_num'] = listSplitResult[0]
            listResult[index]['append_time'] = listSplitResult[1]

            # 依据sign_ids来从htg_childcare_sign表中获取学生id,即student_id, 并加入listResult中的dict中
            strSqlId = "SELECT * FROM htg_childcare_sign WHERE id = " + str(listResult[index].get('sign_ids'))
            listResultId = doSearchObj.doSearchBySql(strSqlId)

            if len(listResultId) == 0:
                del listResult[index]
                continue
            else:
                listResult[index]['student_id'] = listResultId[0].get('_studentid')

            # 依据刚存入的student_id来从htg_users表中获取学生姓名，即name, 并加入listResult中的dict中
            strSqlName = "SELECT * FROM htg_users WHERE id = " + str(listResult[index]['student_id'])
            listResultName = doSearchObj.doSearchBySql(strSqlName)

            if len(listResultName) == 0:
                del listResult[index]
                continue
            else:
                listResult[index]['name'] = listResultName[0].get('name')

            # 根据情况拼接url.这里if...in是区分大小写的
            strUrl = str(listResult[index].get('pic_url'))
            if strUrl != '':
                if 'qiniukey' in strUrl:

                    '''
                    七牛的不需要下载
                    strQnTotalUrl = self.strQnUrl + strUrl
                    listResult[index]['total_url'] = strQnTotalUrl
                    '''
                    listResult[index]['total_url'] = 'qn-no'
                else:
                    strHtgTotalUrl = self.strHtgUrl + strUrl
                    listResult[index]['total_url'] = strHtgTotalUrl
            else:
                strTotalUrl = 'no'
                listResult[index]['total_url'] = strTotalUrl

            # print("--->" + str(index))

        self.logUtil.writerLog("全部所需数据获取完成")
        self.logUtil.writerLog("第一条数据变为: " + str(listResult[0]))
        self.logUtil.writerLog("本次耗时:" + str(round(time.time() - intIndexTwoTime, 4)) + "s")

        # connectionObjMore.close()

        return listResult

    # def getTotalMsgNew(self, strTotalSql, doSearchObj):
    #
    #     # 更新了sql语句, 通过一条sql语句来拿出所有信息
    #
    #     listResult = doSearchObj.doSearchBySql(strTotalSql)
    #
    #     return listResult


    def doBeginDown(self, listResultTotalMsg, downloadObj):

        strRootPath = "D:/Test/download_img" + "/" + self.strImgDirName
        dictShowMsg = {}

        intTotalStudentNum = 0
        intHasDownloadNum = 0
        intRequestErrNum = 0
        intNotFoundNum = 0
        intNotRequestNum = 0


        intIndexDownTime = time.time()
        self.logUtil.writerLog("--->开始下载图片---" + self.runTime.getDateTime())
        for indexTotalMsg in range(len(listResultTotalMsg)):

            print("has download : " + str(indexTotalMsg + 1))
            strPicUrl = str(listResultTotalMsg[indexTotalMsg].get('picUrl'))
            strStudendId = str(listResultTotalMsg[indexTotalMsg].get('studentId'))
            strStudentName = str(listResultTotalMsg[indexTotalMsg].get('studentName'))

            if(strPicUrl != ''):

                if 'qiniukey' in strPicUrl:
                    strTotalUrl = self.strQnUrl + str(strPicUrl.split('qiniukey-')[1])
                else:
                    strTotalUrl = self.strHtgUrl + strPicUrl

                strFirstDirName = "orgId-" + str(listResultTotalMsg[indexTotalMsg].get('orgId'))
                strNextDirName = "shopId-" + str(listResultTotalMsg[indexTotalMsg].get('shopId'))
                strThirdDirName = strStudentName + "-" + strStudendId
                strDateTime = self.runTime.getDataByStampNew(int(listResultTotalMsg[indexTotalMsg].get('appendTime')))
                strImageName = strDateTime + ".jpg"

                strSavePath = self.strImgDirName + strFirstDirName + "/" + strNextDirName + "/" + strThirdDirName
                self.logUtil.writerLog("--> " + str(indexTotalMsg + 1) + "\tstudentName: " + strStudentName + "\tstudentId: " + strStudendId + "\tpicUrl: " + strTotalUrl + "\t准备下载...")
                strResult = downloadObj.downloadImg(strTotalUrl, strSavePath, strImageName)

                if('created' in strResult):
                    intTotalStudentNum += 1
                    if(strResult == 'created-notFound'):
                        intNotFoundNum += 1
                    elif(strResult == 'created-hasDownload'):
                        intHasDownloadNum += 1
                    else:
                        intRequestErrNum += 1
                else:
                    if(strResult == 'needNotCreate-notFound'):
                        intNotFoundNum += 1
                    elif(strResult == 'needNotCreate-hasDownload'):
                        intHasDownloadNum += 1
                    else:
                        intRequestErrNum += 1


            else:
                intNotRequestNum += 1
                self.logUtil.writerLog(str(indexTotalMsg + 1) + "\tstudentName : " + strStudentName + "\tstudentId : " + strStudendId + "\tpicUrl为空,不执行下载")



        strIntervalTime = self.runTime.getIntervalTime(intIndexDownTime)

        self.logUtil.writerLog("--->全部下载完成---" + self.runTime.getDateTime())
        self.logUtil.writerLog("下载图片耗时: " + strIntervalTime)
        self.logUtil.writerLog("数据库查询得到的总数: " + str((len(listResultTotalMsg))))
        self.logUtil.writerLog("机构学生总数: " + str(intTotalStudentNum))
        self.logUtil.writerLog("已下载的图片总数: " + str(intHasDownloadNum))
        self.logUtil.writerLog("未找着的图片总数: " + str(intNotFoundNum))
        self.logUtil.writerLog("未进行请求的总数: " + str(intNotRequestNum))


class DownloadUtil:

    # 下载类

    def __init__(self, logUtilObj):

        self.logUtilObj = logUtilObj

    def downloadImg(self, strImgUrl, strSavePath, strImageName):

        # 下载并保存图片
        # strImgUrl: 图片url
        # strSavePath: 图片存放路径名和图片名字
        # 返回一个状态

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

        intWhetherExist = self.logUtilObj.checkAndCreateDir(strSavePath)
        if(intWhetherExist == 1):
            strResult = 'needNotCreate-'
        else:
            strResult = 'created-'

        try:

            os.chdir(strSavePath)
            requestObj = urllib.request.Request(strImgUrl, None, header)
            responseObj = urllib.request.urlopen(requestObj)
            imgObj = responseObj.read()

        except:
            os.chdir(strOldPath)
            self.logUtilObj.writerLog(strImageName + "请求出错.未下载")
            strResult += 'requestError'

        else:
            if('code' in str(imgObj)):
                os.chdir(strOldPath)
                self.logUtilObj.writerLog(strImageName + "未找到图片,未下载")
                strResult += 'notFound'
            else:
                with open(strImageName, 'wb') as fileObj:
                    fileObj.write(imgObj)

                strResult += 'hasDownload'
                os.chdir(strOldPath)
                self.logUtilObj.writerLog(strImageName + "---->下载完成---" + (str(round(time.time() - intIndexDownTime / 1000, 4)) + "s"))

        # os.chdir(strOldPath)

        return strResult
        # self.logUtilObj.writerLog(strImageName + "---->下载完成---" + str(round(time.time() - intIndexDownTime)/1000, 4) + "s")


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

                if (len(listResult) == 0):
                    self.logUtilObj.writerLog(strSearchSql + "未查找到数据")
                    # listResult = [{'index': 'no'}]
            except:
                self.logUtilObj.writerLog(strSearchSql + "查询时出错")

            finally:
                connectionObj.close()
                self.logUtilObj.writerLog("查询连接已关闭")

        runTime = RunTime()
        strIntervalTime = runTime.getIntervalTime(intIndexDownTime)

        self.logUtilObj.writerLog("本次查询耗时: " + strIntervalTime)

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
                fileObj.write(strContent + '\n')
        else:
            with open(self.strLogFileName, 'w', encoding='utf-8') as fileObj:
                fileObj.write(strContent)

    def checkAndCreateDir(self, strDirName):

        if(not (os.path.exists(strDirName))):
            os.makedirs(strDirName)
            self.writerLog(strDirName + "文件夹不存在,已自动创建")
            intResult = 0
        else:
            intResult = 1

        return intResult


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


    def getIntervalTime(self, intOldTime):

        # 获取时间间隔
        # intOldTime = time.time(), 为过去的

        floatInterval = time.time() - intOldTime
        strIntervalSec = str(round(floatInterval, 2)) + "sec\t"


        if(floatInterval >= 60 and floatInterval < 3600):
            strIntervalTime = strIntervalSec + (str(round(floatInterval/60, 2)) + "min")
        elif(floatInterval >= 3600):
            strIntervalTime = strIntervalSec + (str(round(floatInterval/3600, 2)) + "hour")
        else:
            strIntervalTime = strIntervalSec

        return strIntervalTime



downloadImg = DownloadImg()