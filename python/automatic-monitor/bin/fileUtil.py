import os
import xml.dom.minidom
import configparser

#author: cg
#time: 2017-09-30

class FileUtil:

    configurePath = '../conf'
    configureFileName = 'monitor.conf'

    def __init__(self, strDateTime, strlogContentSecondName, strlogContentName,
                 strlogErrName, strlogErrSecondName):

        strLogPath = self.getLogPath()
        
        self.strDateTime = strDateTime
        self.strlogContentSecondName = strLogPath + '/' + strlogContentSecondName
        self.strlogContentName = strLogPath + '/' + strlogContentName
        self.strlogErrName = strLogPath + '/' + strlogErrName
        self.strlogErrSecondName = strLogPath + '/' + strlogErrSecondName

    def writerContent(self, strContent, strFileMark='Hour', whetherAdd=True):
        
        #strFileMark: 区分写入小时执行的文件还是分钟执行的文件
        #strContent: 写入文件的内容
        #whetherAdd: 是否在文件后面换行追加，默认True
        
        if(strFileMark == 'Hour'):
            if(whetherAdd & True):
                fileObj = open(self.strlogContentName, 'a')
                fileObj.write(strContent + "\n")
                fileObj.close()
            else:
                fileObj = open(self.strlogContentName, 'w')
                fileObj.write(strContent)
                fileObj.close()
        else:
            if(whetherAdd & True):
                fileObj = open(self.strlogContentSecondName, 'a')
                fileObj.write(strContent + "\n")
                fileObj.close()
            else:
                fileObj = open(self.strlogContentSecondName, 'w')
                fileObj.write(strContent)
                fileObj.close()

    def writerErr(self, strContent, strFileMark='Hour', whetherAdd=True):

        if(strFileMark == 'Hour'):
            if(whetherAdd & True):
                fileObj = open(self.strlogErrName, 'a')
                fileObj.write("\n" + strContent)
                fileObj.close()
            else:
                fileObj = open(self.strlogErrName, 'w')
                fileObj.write(strContent)
                fileObj.close()
        else:
            if(whetherAdd & True):
                fileObj = open(self.strlogErrSecondNam, 'a')
                fileObj.write("\n" + strContent)
                fileObj.close()
            else:
                fileObj = open(self.strlogErrSecondNam, 'w')
                fileObj.write(strContent)
                fileObj.close()
            
    

    def getXMLTagElementValue(self, strFilePath, strTagName, strTagElementName, intTagIndex):

        #获取xml文件指定标签的内容，返回一个字符串值
        #self: 对象本身
        #strTagName: 标签名字
        #strTagElementName: 标签中的元素名字
        #intTagIndex: 文件中出现该标签的序列号(即第几个，从0开始)
        
        confObj = xml.dom.minidom.parse(strFilePath)

        documentElementObj = confObj.documentElement
        listElementItem = documentElementObj.getElementsByTagName(strTagName)
        #按照顺序存放，文件内容中第一个出现该标签名字的就放在集合的下标为0的位置
        tagElement = listElementItem[intTagIndex]
        strTagElementValue = tagElement.getAttribute(strTagElementName)
        print(strTagElementName + "=" + strTagElementValue)
        return strTagElementValue


    def getConfFileValue(self, configParserObj, configureFileNameAndPath):

        #获取conf后缀的配置文件内容，返回一个字典
        #configParserObj: 读取配置文件的对象
        #configureFileNameAndPath: 配置文件路径

        dictConfMsg = {}
        intMark = self.checkFileExists(configureFileNameAndPath)
        if(intMark == 1):
            configParserObj.read(configureFileNameAndPath)
            try:
                listSectionName = configParserObj.sections()
            except:
                print("读取配置文件出错")
            else:
                for sectionItem in listSectionName:
                    print(sectionItem)
                    listKeyName = configParserObj.options(sectionItem)
                    print(listKeyName)
                    sectionObj = configParserObj[sectionItem]
                    if(len(listKeyName) != 0):
                        for keyItem in  listKeyName:
                            valueItem = sectionObj[keyItem]
                            if(valueItem == None):
                                dictConfMsg[sectionItem] = listKeyName
                            else:
                                dictConfMsg[keyItem] = valueItem
                    else:
                        dictConfMsg[sectionItem] = ''
        return dictConfMsg


    def initConfigureFile(self):
        
        #初始化配置文件

        strTomcatPath = "/home/liying/dev/tomcat-7.0.73"
        strNginxPath = "/usr/local/nginx"
        strRedisPath = "/home/liying/dev/redis-2.8.24"

        strSmtp_server = "smtp.qq.com"
        strEmail_sendAddr = "yakult-cg@qq.com"
        strEmail_sendPasswd = "lscgsbnjddtgdegc"
        
        strToEmail = "1542723438@qq.com"
        strToEmail2 = "1732821152@qq.com"
        
        strLogPath = "../logs"

        strAuthor = "cg"
        strCreateTime = "2017-09-30"

        if not os.path.exists(self.configurePath):
            os.mkdir(self.configurePath)

        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName

        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        config.add_section('ProjectConfigure')
        config.add_section('LogConfigure')
        config.add_section('EmailConfigure')
        config.add_section('ToEmail')
        config.add_section("Message")
        
        config.set('ProjectConfigure', 'tomcatPath', strTomcatPath)
        config.set('ProjectConfigure', 'nginxPath', strNginxPath)
        config.set('ProjectConfigure', 'redisPath', strRedisPath)
        
        config.set('LogConfigure', 'logPath', strLogPath)

        config.set('EmailConfigure', 'smtp_server', strSmtp_server)
        config.set('EmailConfigure', 'email_sendAddr', strEmail_sendAddr)
        config.set('EmailConfigure', 'email_sendPasswd', strEmail_sendPasswd)
        
        config.set('ToEmail', strToEmail)
        config.set('ToEmail', strToEmail2)

        config.set('Message', 'Author', strAuthor)
        config.set('Message', 'CreateTime', strCreateTime)

        with open(configureFileNameAndPath, 'w') as configureFile:
            config.write(configureFile, space_around_delimiters=True)

        #print("done")


    def checkFileExists(self, configureFileNameAndPath):

        #检测配置文件是否存在，不存在则返回-1

        intMark = -1
        if(os.path.exists(configureFileNameAndPath)):
            intMark = 1

        return intMark

    def checkAndInitConfigure(self, configureFileNameAndPath):

        #检测并初始化配置文件

        intMark = self.checkFileExists(configureFileNameAndPath)
        if(intMark != 1):
            self.initConfigureFile()

    def checkAndCreate(self, FileNameAndPath):

        #检测并创建日志文件路径

        intMark = self.checkFileExists(FileNameAndPath)
        if(intMark != 1):
            print("配置的日志文件夹路径不存在，将自动创建")
            os.mkdir(FileNameAndPath)

    def getLogPath(self):
        
        #获取日志文件配置
        #需要运行的项目字典,即过滤完后的字典
        #dictConfMsg = self.getNeedRunMsg()
        #strLogPath = dictConfMsg.get('logpath')
        strLogPath = ''
        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName
        self.checkAndInitConfigure(configureFileNameAndPath)
        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        config.read(configureFileNameAndPath)
        if(config.has_section('LogConfigure')):
            strLogPath = config['LogConfigure']['logPath']
            self.checkAndCreate(strLogPath)
        else:
            print("配置文件内容缺少日志配置参数")
        return strLogPath
        

    def readConfigureFile(self):

        #读取脚本配置文件
        dictConfMsgTotal = {}
        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName
        self.checkAndInitConfigure(configureFileNameAndPath)
        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        dictConfMsg = self.getConfFileValue(config, configureFileNameAndPath)
        dictConfMsgTotal.update(dictConfMsg)
        if(len(dictConfMsgTotal)  == 0):
            print("未获取到配置文件内容")

        return dictConfMsgTotal

    def getNeedRunMsg(self):

        #根据配置文件的配置内容来选择代码执行
        #即从存放的字典中去除不需要检测运行的项目(配置文件中已经注释掉的)，之后返回
        
        #fileUtil = FileUtil()
        dictConfMsg = self.readConfigureFile()
        print(dictConfMsg)
        intMark = self.checkConfMsg(dictConfMsg)
        if(intMark == 1):
            intTomcatMark = self.checkRunProject("tomcat", "tomcatpath", dictConfMsg)
            if(intTomcatMark == 0):
                del dictConfMsg['tomcatpath']

            intNginxMark = self.checkRunProject("nginx", "nginxpath", dictConfMsg)
            if((intNginxMark == 0)):
                del dictConfMsg['nginxpath']

            intRedisMark = self.checkRunProject("redis", "redispath", dictConfMsg)
            if(intRedisMark == 0):
                del dictConfMsg['redispath']

        print("需要运行的有")
        print(dictConfMsg)
        return dictConfMsg


    def checkConfMsg(self, dictConfMsg):

        #检测配置文件是否完全
        #其中日志路径和email值必须存在
        #所以这里只检查logpath和email
        
        intMark = -1
        if(len(dictConfMsg) != 0):
            
            if(('logpath' in dictConfMsg) & ('ToEmail' in dictConfMsg)):
                if((dictConfMsg.get('logpath') != '') & (len(dictConfMsg.get('ToEmail')) != 0)):
                    intMark = 1
                else:
                    intMark = 0
                    print("未读取到配置参数的值，请更改配置文件")
            else:
                print("配置文件内容缺少配置参数")
        else:
            print("未获取到配置文件内容")
        return intMark


    def checkRunProject(self, projectName, strKey, dictConfMsg):

        #根据配置文件的配置，判断并选择代码块来执行
        #如果返回值为1，则表示返回允许执行检测projectName这个项目

        intMark = -1
        if(strKey in dictConfMsg):
            if(dictConfMsg.get(strKey) != ''):
                intMark = 1
            else:
                intMark = 0
                print("未读取到%s配置参数，请更改配置文件" %(projectName))
        return intMark

    def writerTail(self, strFileName, strDateTime):

        strContentLine = "===================="
        self.writerContent(strFileName, strContentLine)
        
        strContentName = "林繁"
        self.writerContent(strFileName, strContentName)

        self.writerContent(strFileName, strDateTime)

