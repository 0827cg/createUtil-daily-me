#!/usr/bin/python3
#coding=utf-8

import subprocess
import os
from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class TomcatOperate:

    def __init__(self, strTotalPath, intDateMin, fileUtilObj):

        self.fileUtil = fileUtilObj
        self.intDateMin = intDateMin
        self.strTotalPath = strTotalPath

        intCheckResult = self.fileUtil.checkFileExists(self.strTotalPath)
        if(intCheckResult == 1):
            self.checkTomcat()
        else:
            self.fileUtil.writerContent("配置的tomcat路径不存在", 'runErr')
    
    def checkTomcat(self):

        strTomcatStatus = self.getTomcatStatus()
        dictTomcatMsg = self.getTomcatMsg(self.strTotalPath)
        listTomcatName = dictTomcatMsg.get('tomcatName')
        listTomcatPort = dictTomcatMsg.get('tomcatPort')
        listTomcatPath = dictTomcatMsg.get('tomcatPath')
        
        if(self.intDateMin == 30):
            for i in range(len(listTomcatPort)):
                intMark = self.checkTomcatStatusByPort(i, listTomcatName, listTomcatPort, strTomcatStatus)
                if(intMark == 1):
                    self.checkTomcatLogStatusByTomcatName(i, listTomcatName, listTomcatPort)
        else:
            for i in range(len(listTomcatPort)):
                #print(i)
                intMark = self.checkTomcatStatusByPort(i, listTomcatName, listTomcatPort,
                                                       strTomcatStatus, 'Second')
                if(intMark != 1):
                    self.tryStartTomcat(i, listTomcatPath, listTomcatName)

                    
    def getTomcatStatus(self):

        tomcatStatusCL = "ps -ef | grep tomcat"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(tomcatStatusCL)
        strTomcatStatus = dictResult.get('stdout')
        return strTomcatStatus


    def checkTomcatStatusByPort(self, intIndex, listTomcatName, listTomcatPort, strTomcatStatus,
                                strFileMark='Hour'):

        intMark = -1

        if(strTomcatStatus.find(listTomcatName[intIndex]) != -1):
            intMark = 1
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent(("%s在运行" %(listTomcatName[intIndex])), 'Hour', False)
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent(("%s未运行" %(listTomcatName[intIndex])))
            else:
                self.fileUtil.writerContent(("%s未运行" %(listTomcatName[intIndex])), 'Second')

        return intMark


    def checkTomcatLogStatusByTomcatName(self, intIndex, listTomcatName, listTomcatPort):

        intMark = 1

        strOperateTomcatPath = listTomcatPath[intIndex]

        checkLogCL = "tail -n 200 " + strOperateTomcatPath + "/logs/catalina.out"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(checkLogCL)
        strOut = dictResult.get('stdout')
        if(strOut.find("exception") != -1):
            intMark = -1
            self.fileUtil.writerContent(("%s日志输出异常" %(listTomcatName[intIndex])))
        else:
            self.fileUtil.writerContent(("%s日志输出正常" %(listTomcatName[intIndex])))
            self.fileUtil.writerErr(strOut)
        return intMark
        


    def tryStartTomcat(self, intIndex, listTomcatPath, listTomcatName):

        intMark = -1

        self.fileUtil.writerContent("脚本尝试将其启动....", 'Second')
        strOperateTomcatPath = listTomcatPath[intIndex]
        tryStartTomcatCL = strOperateTomcatPath + "/bin/./catalina.sh start"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(tryStartTomcatCL)
        strOut = dictResult.get('stdout')
        strErr = dictResult.get('stderr')
        if(strOut != ''):
            if((strOut.find('Tomcat started') != -1) & (strErr == '')):
                self.fileUtil.writerContent(("%s已被脚本启动成功" %(listTomcatName[intIndex])),
                                            'Second')
                intMark = 1
            else:
                self.fileUtil.writerContent(("脚本启动%s未成功,请手动启动" %(listTomcatName[intIndex])),
                                            'Second')
                self.fileUtil.writerErr(strErr, 'Second')
        else:
            self.fileUtil.writerContent(("%s启动命令未执行,请手动执行" %(listTomcatName[intIndex])), 'Second')
            self.fileUtil.writerErr(strErr, 'Second')
        return intMark


    def getTomcatMsg(self, strTotalPath):
        
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

