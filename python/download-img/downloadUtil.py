# -*- coding: utf-8 -*-

import urllib.request
import os
import time

class DownloadUtil:

    def __init__(self):

        # self.doWork()
        # self.doWorkNew()
        self.downloadImg('http://sign-pic.file.cdn.haotuoguan.cn/FnDUNwdPnjPKxHW3ZZjtKCMa-GdI', 'img/', 'dd-1.jpg')

    def doWork(self):

        strImgUrlHas = "http://sign-pic.file.cdn.haotuoguan.cn/FrrVZIx-l6IBTZ59c_16cwEmUAFr"
        strImgUrlNo = "http://file.haotuoguan.cn/download?shortid=E1pfQDkFf"
        strRootPath = os.getcwd()
        strSavePath = 'test/do-2/'

        response = urllib.request.urlopen(strImgUrlHas)
        print(response)
        print(response.status)
        print(response.getcode())

        imgObj = response.read()
        print(imgObj)
        print(type(imgObj))
        # print(imaObj.content)
        print(type(imgObj.decode('utf-8')))
        # print(type(eval(imgObj.decode('utf-8'))))
        if (not (os.path.exists(strSavePath))):
            os.makedirs(strSavePath)
        os.chdir(strSavePath)

        # dd = urllib.request.urlretrieve(strImgUrl, 'do.jpg')
        with open('dd.jpg', 'wb') as fileObj:
            fileObj.write(imgObj)

        print('done')

    def doWorkNew(self):

        strImgUrlHas = "http://sign-pic.file.cdn.haotuoguan.cn/FrrVZIx-l6IBTZ59c_16cwEmUAFr"
        strImgUrlNo = "http://file.haotuoguan.cn/download?shortid=E1pfQDkFf"

        strSavePath = 'test/do-2/'

        header = {
            'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/'
                          '604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),
            'Cookie': 'connect.sid=s%3AfUMqGRS0y0ZaEkeLIwAtlVOD2lfQDpmd.hm%2FXSippPDk2g91PkOG1eXpn17ceblg8BdUigVBe6KQ'
        }

        requestObj = urllib.request.Request(strImgUrlHas, None, header)
        response = urllib.request.urlopen(requestObj)
        print(response)
        imgObj = response.read()

        if('code' in str(imgObj)):
            print("无图片")
        else:
            print("有图片")

        print(str(imgObj))
        if (not (os.path.exists(strSavePath))):
            os.makedirs(strSavePath)
        os.chdir(strSavePath)

        # dd = urllib.request.urlretrieve(strImgUrl, 'do.jpg')
        with open('dd.jpg', 'wb') as fileObj:
            fileObj.write(imgObj)

        print('done')


    def downloadImg(self, strImgUrl, strSavePath, strImageName):

        # 下载并保存图片
        # strImgUrl: 图片url
        # strSavePath: 图片存放路径名和图片名字
        # 返回一个状态

        # if strImgUrl == 'no':
        #     print(strSavePath + strImgUrl + "---->未图片链接---->未下载")
        # elif strImgUrl == 'qn-no':
        #     print(strSavePath + strImgUrl + "---->未图片链接---->不下载")
        # else:

        # 很奇怪的问题,try中运行没出错,也会执行except中的代码


        header = {
            'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/'
                           '604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),
            'Cookie': 'connect.sid=s%3AfUMqGRS0y0ZaEkeLIwAtlVOD2lfQDpmd.hm%2FXSippPDk2g91PkOG1eXpn17ceblg8BdUigVBe6KQ'
        }

        intIndexDownTime = time.time()
        strOldPath = os.getcwd()

        intWhetherExist = self.checkAndCreateDir(strSavePath)
        if(intWhetherExist == 1):
            strResult = 'needNotCreate-'
        else:
            strResult = 'created-'

        try:

            os.chdir(strSavePath)
            requestObj = urllib.request.Request(strImgUrl, None, header)
            responseObj = urllib.request.urlopen(requestObj)
            imgObj = responseObj.read()

        except Exception:

            os.chdir(strOldPath)
            print(strImageName + "请求出错.未下载")
            strResult += 'requestError'
        else:

            if ('code' in str(imgObj)):
                os.chdir(strOldPath)
                print(strImageName + "未找到图片,未下载")
                strResult += 'notFound'
            else:
                with open(strImageName, 'wb') as fileObj:
                    fileObj.write(imgObj)

                strResult += 'hasDownload'
                os.chdir(strOldPath)
                print(strImageName + "---->下载完成---" + str(str(round(time.time() - intIndexDownTime / 1000, 4)) + "s"))

        # os.chdir(strOldPath)

        return strResult
        # print(strImageName + "---->下载完成---" + str(round(time.time() - intIndexDownTime)/1000, 4) + "s")

    def checkAndCreateDir(self, strDirName):

        if(not (os.path.exists(strDirName))):
            os.makedirs(strDirName)
            print(strDirName + "文件夹不存在,已自动创建")
            intResult = 0
        else:
            intResult = 1

        return intResult

downloadUtil = DownloadUtil()