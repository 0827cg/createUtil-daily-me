import os

class Test:

    def checkConfigureFileExists(self, configureFileNameAndPath):

        #检测配置文件是否存在，不存在则返回-1

        intMark = -1
        if(os.path.exists(configureFileNameAndPath)):
            intMark = 1
        print(intMark)
        return intMark

    def checkAndCreate(self, configureFileNameAndPath):

        intMark = self.checkConfigureFileExists(configureFileNameAndPath)
        if(intMark != 1):
            os.mkdir(configureFileNameAndPath)

    

configureFileNameAndPath = "../log"
test = Test()
#test.checkConfigureFileExists(configureFileNameAndPath)
test.checkAndCreate(configureFileNameAndPath)
