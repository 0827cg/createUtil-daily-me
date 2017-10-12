#!/usr/bin/python3
#coding=utf-8

from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class NginxOperate:

    def __init__(self, strNginxPath, intDateMin, fileUtilObj):
        
        self.fileUtil = fileUtilObj
        self.intDateMin = intDateMin
        self.strNginxPath = strNginxPath
        intCheckResult = self.fileUtil.checkFileExists(self.strNginxPath)
        if(intCheckResult == 1):
            self.checkNginx()
        else:
            self.fileUtil.writerContent("配置的nginx路径不存在", 'runErr')

    def checkNginx(self):

        strNginxStatus = self.getNginxStatus()

        if(self.intDateMin == 30):
            self.checkNginxStatus(strNginxStatus)
        else:
             intMark = self.checkNginxStatus(strNginxStatus, 'Second')
             if(intMark == -1):
                 self.tryStartNginx(self.strNginxPath)



    def getNginxStatus(self):
        
        nginxStatusCL = "ps -ef | grep nginx"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(nginxStatusCL)
        strNginxStatus = dictResult.get('stdout')
        return strNginxStatus


    def checkNginxStatus(self, strNginxStatus, strFileMark='Hour'):

        intMark = -1
        strNginx = "nginx:"
        
        if(strNginxStatus.find(strNginx) != -1):
            intMark = 1
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("nginx在运行")
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("nginx未运行")
            else:
                self.fileUtil.writerContent("nginx未运行", 'Second')

        return intMark


    def tryStartNginx(self, strNginxPath):
        
        intMark = -1
        self.fileUtil.writerContent("脚本尝试将其启动....", 'Second')
        strStartNginxCL = strNginxPath + "/sbin/./nginx"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(strStartNginxCL)
        strErr = dictResult.get('stderr')
        if(strErr == ''):
            self.fileUtil.writerContent("nginx已被脚本启动", 'Second')
            intMark = 1
        else:
            self.fileUtil.writerContent("脚本启动nginx未成功，请手动启动", 'Second')
            self.fileUtil.writerErr(strErr, 'Second')

        return intMark
        
