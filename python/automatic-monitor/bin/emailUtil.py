import smtplib
from email.mime.text import MIMEText
from email.header import Header

#author: cg
#time: 2017-09-30

class sendEmail:

    def __init__(self, dictMailMsg, fileUtilObj):

        #dictMailMsg:存放发送邮件需要的数据，
        #其中的key有
        #smtp_server:
        #mail_sendAddr:
        #mail_sendPasswd:
        #mail_toAddr:

        self.fileUtilObj = fileUtilObj
        
    def setMsg(self, dictMailMsg):

        for keyItem in dictMailMsg:

            print(keyItem)
