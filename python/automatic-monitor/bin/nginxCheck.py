from fileUtil import FileUtil
from process import ProcessCL

#author: cg
#time: 2017-09-30

class NginxOperate:

    def __init__(self, strNginxPath, intDateMin, fileUtilObj):
        self.strNginxPath = strNginxPath
        self.intDateMin = intDateMin
        self.fileUtil = fileUtilObj

        self.checkNginx()

    def checkNginx(self):

        #每个小时检测一遍，不做操作
        #其他时候，当检测到未运行时，脚本尝试自启一次

        strNginxStatus = self.getNginxStatus()

        if(self.intDateMin == 30):
            self.checkNginxStatus(strNginxStatus)
        else:
             intMark = self.checkNginxStatus(strNginxStatus, 'Second')
             if(intMark == -1):
                 self.tryStartNginx(self.strNginxPath)



    def getNginxStatus(self):
        
        #获取进程中的nginx
        
        nginxStatusCL = "ps -ef | grep nginx"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(nginxStatusCL)
        strNginxStatus = dictResult.get('stdout')
        return strNginxStatus


    def checkNginxStatus(self, strNginxStatus, strFileMark='Hour'):

        #判断nginx是否运行

        intMark = -1
        strNginx = "nginx:"
        
        if(strNginxStatus.find(strNginx) != -1):
            #print("nginx在运行")
            intMark = 1
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("nginx在运行")
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("nginx未运行")
            else:
                self.fileUtil.writerContent("nginx未运行", 'Second')
            #print("nginx未运行")
        return intMark


    def tryStartNginx(self, strNginxPath):

        #脚本启动nginx

        intMark = -1
        self.fileUtil.writerContent("脚本尝试将其启动....", 'Second')
        strStartNginxCL = strNginxPath + "/sbin/./nginx"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(strStartNginxCL)
        strErr = dictResult.get('stderr')
        if(strErr == ''):
            #print("nginx已被脚本启动")
            self.fileUtil.writerContent("nginx已被脚本启动", 'Second')
            intMark = 1
        else:
            #print("脚本启动nginx未成功，请手动启动")
            self.fileUtil.writerContent("脚本启动nginx未成功，请手动启动", 'Second')
            self.fileUtil.writerErr(strErr, 'Second')
            #print(strErr)
        return intMark
        
