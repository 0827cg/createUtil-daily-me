from monitorbin.util.fileUtil import FileUtil
from monitorbin.module.tomcatCheck import TomcatOperate
from monitorbin.module.nginxCheck import NginxOperate
from monitorbin.module.redisCheck import RedisOperate
from monitorbin.util.emailUtil import EmailUtil

#author: cg错过
#time: 2017-09-30

class Operate:

    #选择执行操作类

    def __init__(self):
        
        self.fileUtil = FileUtil()
     
        dictNeedRunMsg = self.fileUtil.getNeedRunMsg()
        if(len(dictNeedRunMsg) > 1):
            self.runProcess(dictNeedRunMsg)
            emailUtil = EmailUtil(dictNeedRunMsg, self.fileUtil)
        elif(len(dictNeedRunMsg) == 1):
            self.fileUtil.writerContent("配置文件参数值不全", 'runErr')
        else:
            self.fileUtil.writerContent("配置文件读取失败", 'runErr')


    def runProcess(self, dictNeedRunMsg):

        #运行检测各个项目
        
        listKeys = dictNeedRunMsg.keys()
        for keyItem in listKeys:
            if(keyItem.find('tomcat') != -1):
                strTomcatPath = dictNeedRunMsg.get(keyItem)
                tomcatOperate = TomcatOperate(strTomcatPath, self.fileUtil.strMinTime, self.fileUtil)
                #print(strTomcatPath)
            if(keyItem.find('nginx') != -1):
                strNginxPath = dictNeedRunMsg.get(keyItem)
                nginxOperate = NginxOperate(strNginxPath, self.fileUtil.strMinTime, self.fileUtil)
                #print(strNginxPath)
            if(keyItem.find('redis') != -1):
                strRedisPath = dictNeedRunMsg.get(keyItem)
                redisOperate = RedisOperate(strRedisPath, self.fileUtil.strMinTime, self.fileUtil)
                #print(strRedisPath)
