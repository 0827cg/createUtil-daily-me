#!/usr/bin/python3
#coding=utf-8

import sys
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

#author: cg错过
#time: 2017-09-30

class EmailUtil:

    def __init__(self, dictNeedRunMsg, fileUtilObj):

        self.fileUtilObj = fileUtilObj
        dictEmailMsg = self.getForEmailMsg(dictNeedRunMsg)
        listEmailContentMsg = self.checkAndGetForEmailListMsg()

        strServerName = dictEmailMsg.get('servername')
        strUserName = dictEmailMsg.get('username')
        listNewEmailContentMsg = self.fileUtilObj.reWriterForEmail(listEmailContentMsg, dictEmailMsg)
        
        self.choiceSend(dictEmailMsg, listNewEmailContentMsg)
        
    def getForEmailMsg(self, dictNeedRunMsg):

        dictMsgForEmail = {}
        for keyItem in dictNeedRunMsg:
            if((keyItem == 'email_sendaddr') | (keyItem == 'email_sendpasswd') |
               (keyItem == 'smtp_server') | (keyItem == 'ToEmail') | (keyItem == 'logpath') |
               (keyItem == 'servername') | (keyItem == 'username')):
                dictMsgForEmail[keyItem] = dictNeedRunMsg.get(keyItem)
    
        return dictMsgForEmail

    def checkAndGetForEmailListMsg(self):

        listSendContent = []
        intExistsContent = self.fileUtilObj.checkFileExists(self.fileUtilObj.strlogContentName)
        intExistsContentS = self.fileUtilObj.checkFileExists(self.fileUtilObj.strlogContentSecondName)
        if(intExistsContent == 1):
            listSendContent.append('Hour')
            print(self.fileUtilObj.strlogContentName)
            strContent = self.fileUtilObj.readFileContent(self.fileUtilObj.strlogContentName)
            listSendContent.append(strContent)
            
            intExistsErr = self.fileUtilObj.checkFileExists(self.fileUtilObj.strlogErrName)
            if(intExistsErr == 1):
                listSendContent.append(self.fileUtilObj.strlogErrName)

        elif(intExistsContentS == 1):
            listSendContent.append('Second')
            print(self.fileUtilObj.strlogContentSecondName)
            strContentS = self.fileUtilObj.readFileContent(self.fileUtilObj.strlogContentSecondName)
            listSendContent.append(strContentS)
            
            intExistsErrS = self.fileUtilObj.checkFileExists(self.fileUtilObj.strlogErrSecondName)
            if(intExistsErrS == 1):
                listSendContent.append(self.fileUtilObj.strlogErrSecondName)

        else:
            listSendContent.append('no')
            strContent = "未产生日志文件"
            self.fileUtilObj.writerContent("未产生日志文件", 'runErr')
            listSendContent.append(strContent)
        print("未重构......")
        print(listSendContent)

        return listSendContent


    def choiceSend(self, dictEmailMsg, listEmailContent):

        strSmtpServer = dictEmailMsg.get('smtp_server')
        strSendAddr = dictEmailMsg.get('email_sendaddr')
        strPasswd = dictEmailMsg.get('email_sendpasswd')
        listToAddr = dictEmailMsg.get('ToEmail')
        strSubject = listEmailContent[1]
        strContent = listEmailContent[2]

        if(len(listEmailContent) == 3):
            if(listEmailContent[0] != 'no'):
                self.sendEmailByString(strSmtpServer, strSendAddr, strPasswd,
                               listToAddr, strSubject, strContent)
            else:
                self.fileUtilObj.writerContent("邮件未发送", 'runErr')
        else:
            strErrFilePath = listEmailContent[3]
            self.sendEmailByStringAndFile(strSmtpServer, strSendAddr, strPasswd,
                               listToAddr, strSubject, strContent, strErrFilePath)


    def sendEmailByString(self, strSmtpServer, strSendAddr, strPasswd,
                          listToAddr, strSubject, strContent):

        #mail_port = '465'
        
        message = MIMEText(strContent, "plain", "utf-8")
        message['Subject'] = Header(strSubject, 'utf-8')
        message['From'] = Header('monitor<%s>' % strSendAddr, 'utf-8')
        message['To'] = Header('monitor.admin', 'utf-8')

        try:
            smtpObj = SMTP_SSL(strSmtpServer)
            #smtpObj.set_debuglevel(1)
            smtpObj.ehlo(strSmtpServer)
            smtpObj.login(strSendAddr, strPasswd)
            if(len(listToAddr) > 0):
                smtpObj.sendmail(strSendAddr, listToAddr, message.as_string())
                smtpObj.quit()
            else:
                self.fileUtilObj.writerContent("接收邮件地址为空", 'runErr')
        except:
            print(sys.exc_info()[0])
            self.fileUtilObj.writerContent("邮件发送失败", 'runErr')


    def sendEmailByStringAndFile(self, strSmtpServer, strSendAddr, strPasswd,
                          listToAddr, strSubject, strContent, strErrFilePath):
        
        #mail_port = '465'

        message = MIMEMultipart()
        message['Subject'] = Header(strSubject, 'utf-8')
        message['From'] = Header('monitor<%s>' % strSendAddr, 'utf-8')
        message['To'] = Header('monitor.admin', 'utf-8')

        message.attach(MIMEText(strContent, 'plain', 'utf-8'))

        annexFile = MIMEText(open(strErrFilePath, 'rb').read(), 'base64', 'utf-8')
        annexFile["Content-Type"] = 'application/octet-stream'
        annexFile["Content-Disposition"] = 'attachment; filename="err_logs.txt"'
        message.attach(annexFile)

        try:
            smtpObj = SMTP_SSL(strSmtpServer)
            #smtpObj.set_debuglevel(1)
            smtpObj.ehlo(strSmtpServer)
            smtpObj.login(strSendAddr, strPasswd)
            if(len(listToAddr) > 0):
                smtpObj.sendmail(strSendAddr, addrItem, message.as_string())
                smtpObj.quit()
            else:
                self.fileUtilObj.writerContent("接受邮件地址为空", 'runErr')
        except:
            print(sys.exc_info()[0])
            self.fileUtilObj.writerContent("附件邮件发送失败", 'runErr')
        
        
