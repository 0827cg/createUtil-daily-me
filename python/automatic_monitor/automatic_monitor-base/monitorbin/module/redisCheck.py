import os
from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class RedisOperate:

    #redis检测模块
    
    def __init__(self, strRedisPath, intDateMin, fileUtilObj):

        self.fileUtil = fileUtilObj
        self.intDateMin = intDateMin
        self.strRedisPath = strRedisPath
        intCheckResult = self.fileUtil.checkFileExists(self.strRedisPath)
        if(intCheckResult == 1):
            self.checkRedis()
        else:
            self.fileUtil.writerContent("配置的redis路径不存在", 'runErr')

    def checkRedis(self):

        strRedisStatus = self.getRedisStatus()

        if(self.intDateMin == 30):
            self.checkRedisStatus(strRedisStatus)
        else:
            intMark = self.checkRedisStatus(strRedisStatus, 'Second')
            if(intMark == -1):
                self.tryStartRedis(self.strRedisPath)


    def getRedisStatus(self):

        redisStatusCL = "ps -ef | grep redis"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(redisStatusCL)
        strRedisStatus = dictResult.get('stdout')
        return strRedisStatus


    def checkRedisStatus(self, strRedisStatus, strFileMark='Hour'):

        intMark = -1
        strRedis = "redis-server"

        if(strRedisStatus.find(strRedis) != -1):
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("redis在运行")
            intMark = 1
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("redis未运行")
            else:
                self.fileUtil.writerContent("redis未运行", 'Second')
        return intMark


    def tryStartRedis(self, strRedisPath):
        
        intMark = -1
        
        self.fileUtil.writerContent("脚本尝试将其启动....", 'Second')
        strStartRedisCL = strRedisPath + "/src/./redis-server"
        processCL = ProcessCL()
        dictResult = processCL.getContinueResultAndProcess(strStartRedisCL)
        strOut = dictResult.get('stdout')
        strErr = dictResult.get('stderr')
        if(strOut.find('redis.io') != -1):
            self.fileUtil.writerContent("redis已被脚本启动", 'Second')
            intMark = 1
        else:
            self.fileUtil.writerContent("脚本启动redis未成功，请手动启动", 'Second')
            self.fileUtil.writerErr(strErr, 'Second')

        return intMark
        
        
