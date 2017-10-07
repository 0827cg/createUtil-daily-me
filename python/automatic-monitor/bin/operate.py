from fileUtil import FileUtil
from tomcatCheck import TomcatOperate
from nginxCheck import NginxOperate
from redisCheck import RedisOperate
from sysTime import RunTime

#author: cg
#time: 2017-09-30

class Operate:

    def __init__(self):
        
        runTime = RunTime()
        self.strMinTime = runTime.getMinTime()
        self.strDateTime = runTime.getDateTime()
        self.strNumSecondTime = runTime.getNumSecondTime()
        self.strNumHourTime = runTime.getNumHourTime()
        
        self.setFileName()
        
        self.fileUtil = FileUtil(self.strDateTime, self.strlogContentSecondName,
                            self.strlogContentName, self.strlogErrName, self.strlogErrSecondName)
        dictNeedRunMsg = self.fileUtil.getNeedRunMsg()
        
        listKeys = dictNeedRunMsg.keys()
        for keyItem in listKeys:
            if(keyItem.find('tomcat') != -1):
                strTomcatPath = dictNeedRunMsg.get(keyItem)
                #tomcatOperate = TomcatOperate(strTomcatPath, self.strMinTime, self.fileUtil)
                print(strTomcatPath)
            if(keyItem.find('nginx') != -1):
                strNginxPath = dictNeedRunMsg.get(keyItem)
                #nginxOperate = NginxOperate(strNginxPath, self.strMinTime, self.fileUtil)
                print(strNginxPath)
            if(keyItem.find('redis') != -1):
                strRedisPath = dictNeedRunMsg.get(keyItem)
                #redisOperate = RedisOperate(strRedisPath, self.strMinTime, self.fileUtil)
                print(strRedisPath)


    def setFileName(self):

        self.strlogContentSecondName = "monitor_content-" + self.strNumSecondTime + ".txt"
        self.strlogContentName = "monitor_content-" + self.strNumHourTime + ".txt"
        self.strlogErrName = "monitor_err-" + self.strNumHourTime + ".txt"
        self.strlogErrSecondName = "monitor_err" + self.strNumSecondTime + ".txt"



operate = Operate()
#operate.test()
#operate.getNeedRunMsg()
#print(operate.str1)
