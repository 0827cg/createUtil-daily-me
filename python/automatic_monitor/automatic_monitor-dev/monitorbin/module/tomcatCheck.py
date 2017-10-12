#!/usr/bin/python3
#coding=utf-8

import subprocess
import os
from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class TomcatOperate:

    #tomcat检测模块
    #需要配合前面分时间段来运行
    #即至少要有个对tomcat进行所有全部的检测和部分检测两种功能
    #全检不提供脚本操作功能，例如自启。全检后不管是否正常都将发送邮件
    #部检提供自启，自启后只有检测到不正常才发送邮件

    def __init__(self, strTotalPath, intDateMin, fileUtilObj):
        
        #strTotalPath: tomcat的安装文件根目录的上一级目录
        #intDateMin: 当前运行脚本的分钟数
        #fileUtilObj: FileUtil的对象(脚本从运行到结束都只有这一个FileUtil对象)

        self.fileUtil = fileUtilObj
        self.intDateMin = intDateMin
        self.strTotalPath = strTotalPath
        #self.fileUtil.writerContent("你好")
        intCheckResult = self.fileUtil.checkFileExists(self.strTotalPath)
        if(intCheckResult == 1):
            self.checkTomcat()
        else:
            self.fileUtil.writerContent("配置的tomcat路径不存在", 'runErr')
    
    def checkTomcat(self):

        #检测tomcat

        strTomcatStatus = self.getTomcatStatus()
        dictTomcatMsg = self.getTomcatMsg(self.strTotalPath)
        listTomcatName = dictTomcatMsg.get('tomcatName')
        listTomcatPort = dictTomcatMsg.get('tomcatPort')
        listTomcatPath = dictTomcatMsg.get('tomcatPath')
        
        if(self.intDateMin == 30):
            for i in range(len(listTomcatPort)):
                intMark = self.checkTomcatStatusByPort(i, listTomcatName, listTomcatPort, strTomcatStatus)
                if(intMark == 1):
                    #print("查看日志")
                    #self.fileUtil.writerContent("查看日志")
                    self.checkTomcatLogStatusByTomcatName(i, listTomcatName, listTomcatPort)
        else:
            for i in range(len(listTomcatPort)):
                #print(i)
                intMark = self.checkTomcatStatusByPort(i, listTomcatName, listTomcatPort,
                                                       strTomcatStatus, 'Second')
                if(intMark != 1):
                    #print("重启")
                    self.tryStartTomcat(i, listTomcatPath, listTomcatName)

                    
    def getTomcatStatus(self):
        
        #获取进程中的tomcat
        tomcatStatusCL = "ps -ef | grep tomcat"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(tomcatStatusCL)
        strTomcatStatus = dictResult.get('stdout')
        return strTomcatStatus


    def checkTomcatStatusByPort(self, intIndex, listTomcatName, listTomcatPort, strTomcatStatus,
                                strFileMark='Hour'):

        #检测tomcat是否运行，在运行返回1
        #intIndex: 要检测的tomcat所在dictTomcatMsg中tomcatName的下标
        #dictTomcatMsg: 存放tomcat文件名,端口号和对应路径,为字典类型包含列表

        intMark = -1
        
        #listTomcatName = dictTomcatMsg.get('tomcatName')
        #listTomcatPort = dictTomcatMsg.get('tomcatPort')

        if(strTomcatStatus.find(listTomcatName[intIndex]) != -1):
            intMark = 1
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent(("%s在运行" %(listTomcatName[intIndex])), 'Hour', False)
            #else:
                #self.fileUtil.writerContent(("%s在运行" %(listTomcatName[intIndex])), 'Second')
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent(("%s未运行" %(listTomcatName[intIndex])))
            else:
                self.fileUtil.writerContent(("%s未运行" %(listTomcatName[intIndex])), 'Second')
                #print("%s未运行" %(listTomcatName[intIndex]))

        return intMark


    def checkTomcatLogStatusByTomcatName(self, intIndex, listTomcatName, listTomcatPort):

        #检测tomcat日志输出是否正常，正常返回1
        #intIndex: tomcat所在dictTomcatMsg中tomcatName的下标，一般检测在运行的tomcat
        #dictTomcatMsg: 存放tomcat文件名,端口号和对应路径,为字典类型包含列表

        intMark = 1

        #listTomcatName = dictTomcatMsg.get('tomcatName')
        #listTomcatPort = dictTomcatMsg.get('tomcatPort')
        strOperateTomcatPath = listTomcatPath[intIndex]

        checkLogCL = "tail -n 200 " + strOperateTomcatPath + "/logs/catalina.out"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(checkLogCL)
        strOut = dictResult.get('stdout')
        if(strOut.find("exception") != -1):
            intMark = -1
            #print("%s日志输出异常" %(listTomcatName[intIndex]))
            self.fileUtil.writerContent(("%s日志输出异常" %(listTomcatName[intIndex])))
        else:
            self.fileUtil.writerContent(("%s日志输出正常" %(listTomcatName[intIndex])))
            #print("%s日志输出正常" %(listTomcatName[intIndex]))
            self.fileUtil.writerErr(strOut)
        return intMark
        


    def tryStartTomcat(self, intIndex, listTomcatPath, listTomcatName):

        #启动未运行的tomcat，启动成功返回1
        #intIndex: 未运行的tomcat所在dictTomcatMsg中tomcatName的下标
        #dictTomcatMsg: 存放tomcat文件名,端口号和对应路径，为字典类型包含列表

        intMark = -1

        #listTomcatPath = dictTomcatMsg.get('tomcatPath')
        #listTomcatName = dictTomcatMsg.get('tomcatName')
        #print("脚本尝试将其启动....")
        self.fileUtil.writerContent("脚本尝试将其启动....", 'Second')
        strOperateTomcatPath = listTomcatPath[intIndex]
        tryStartTomcatCL = strOperateTomcatPath + "/bin/./catalina.sh start"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(tryStartTomcatCL)
        strOut = dictResult.get('stdout')
        strErr = dictResult.get('stderr')
        if(strOut != ''):
            if((strOut.find('Tomcat started') != -1) & (strErr == '')):
                #print("%s已被脚本启动成功" %(listTomcatName[intIndex]))
                self.fileUtil.writerContent(("%s已被脚本启动成功" %(listTomcatName[intIndex])),
                                            'Second')
                intMark = 1
            else:
                #print("脚本启动%s未成功,请手动启动" %(listTomcatName[intIndex]))
                self.fileUtil.writerContent(("脚本启动%s未成功,请手动启动" %(listTomcatName[intIndex])),
                                            'Second')
                self.fileUtil.writerErr(strErr, 'Second')
        else:
            #print("%s启动命令未执行" %(listTomcatName[intIndex]))
            self.fileUtil.writerContent(("%s启动命令未执行,请手动执行" %(listTomcatName[intIndex])), 'Second')
            #print(strErr)
            self.fileUtil.writerErr(strErr, 'Second')
        return intMark


    def getTomcatMsg(self, strTotalPath):
        
        #根据存放多个tomcat的文件路径来查找多少个tomcat
        #获取tomcat安装文件的名称和对应的端口
        #通过读取tomcat配置文件，以此来获得端口号
        #返回一个字典，存放tomcat安装文件名和对应端口号
        
        dictTomcatMsg = {}
        listTomcatName = []
        listMsgName = os.listdir(strTotalPath)
        for item in listMsgName:
            nextPath = (strTotalPath + '/' +  item)
            if(os.path.isdir(nextPath)):
                confPath = (nextPath + '/conf/server.xml')
                if((item.find("tomcat") != -1) & (os.path.exists(confPath))):
                    listMsgName.remove(item)
                    listTomcatName.append(item)

        #fileUtil = FileUtil()
        listTomcatPort = []
        listTomcatPath = []
        for item in listTomcatName:
            nextPath = (strTotalPath + '/' +  item)
            confPath = (nextPath + '/conf/server.xml')
            intItemPort = self.fileUtil.getXMLTagElementValue(confPath, 'Connector', 'port', 0)
            listTomcatPort.append(intItemPort)
            listTomcatPath.append(nextPath)

        dictTomcatMsg['tomcatName'] = listTomcatName
        dictTomcatMsg['tomcatPort'] = listTomcatPort
        dictTomcatMsg['tomcatPath'] = listTomcatPath
        print(dictTomcatMsg)
        
        return dictTomcatMsg

