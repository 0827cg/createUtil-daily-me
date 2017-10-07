import os
from fileUtil import FileUtil
from process import ProcessCL

#author: cg
#time: 2017-09-30

class RedisOperate:

    
    def __init__(self, strRedisPath, intDateMin, fileUtilObj):
        self.strRedisPath = strRedisPath
        self.intDateMin = intDateMin
        self.fileUtil = fileUtilObj

        self.checkRedis()    

    def checkRedis(self):

        #每个小时检测一遍，不做操作
        #其他时候，当检测到未运行时，脚本尝试自启一次

        strRedisStatus = self.getRedisStatus()

        if(self.intDateMin == 30):
            self.checkRedisStatus(strRedisStatus)
        else:
            intMark = self.checkRedisStatus(strRedisStatus, 'Second')
            if(intMark == -1):
                self.tryStartRedis(self.strRedisPath)


    def getRedisStatus(self):

        #获取进程中的redis

        redisStatusCL = "ps -ef | grep redis"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(redisStatusCL)
        strRedisStatus = dictResult.get('stdout')
        return strRedisStatus


    def checkRedisStatus(self, strRedisStatus, strFileMark='Hour'):

        #判断redis是否允许

        intMark = -1
        strRedis = "redis-server"

        if(strRedisStatus.find(strRedis) != -1):
            #print("redis在运行")
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("redis在运行")
            intMark = 1
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("redis未运行")
            else:
                self.fileUtil.writerContent("redis未运行", 'Second')
            print("redis未运行")
        return intMark


    def tryStartRedis(self, strRedisPath):

        #脚本启动redis

        intMark = -1
        #print("脚本尝试将其启动....")
        #print(strRedisPath)
        self.fileUtil.writerContent("脚本尝试将其启动....", 'Second')
        strStartRedisCL = strRedisPath + "/src/./redis-server"
        processCL = ProcessCL()
        dictResult = processCL.getContinueResultAndProcess(strStartRedisCL)
        strOut = dictResult.get('stdout')
        strErr = dictResult.get('stderr')
        if(strOut.find('redis.io') != -1):
            self.fileUtil.writerContent("redis已被脚本启动", 'Second')
            #print("redis已被脚本启动成功")
            intMark = 1
        else:
            #print("脚本启动redis未成功，请手动启动")
            self.fileUtil.writerContent("脚本启动redis未成功，请手动启动", 'Second')
            self.fileUtil.writerErr(strErr, 'Second')
            #print(strErr)
        return intMark
        
        
