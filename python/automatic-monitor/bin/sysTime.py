import time

#author: cg
#time: 2017-09-30

class RunTime:

    def getTime(self, strFormat):

        #按照格式获取时间

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime

    def getDateTime(self):
        return self.getTime("%Y-%m-%d %H:%M:%S")

    def getNumSecondTime(self):
        return self.getTime("%Y%m%d%H%M%S")

    def getNumHourTime(self):
        return self.getTime("%Y%m%d%H")

    def getMinTime(self):
        return self.getTime("%M")
