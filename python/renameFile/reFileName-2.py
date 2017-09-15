import os
import sys
import time

#author:cg错过   2016-12-30

def main():

    copyFile(reFileName())
    

def reFileName():

#获取文件名字和文件创建的时间,返回一个二维序列

    allIndex = 0
    
    filePath = os.getcwd()
    fileList = os.listdir(filePath)
    fileNameList = []
    fileTimeList = []
    
    
    allFileMsg = []

    for fileElement in fileList:
            
        index = 0

        fileMsg = []
        addFilePath = os.path.join(filePath, fileElement)
        if os.path.isdir(addFilePath):
            continue
        
        fileType = os.path.splitext(fileElement)[1]
        
        if fileType == '.png':
            
            fileInfo = os.stat(fileElement)
            
            fileTime = time.localtime(fileInfo.st_ctime)
            strFileTime = (str(fileTime.tm_year) + '-' +
                  str(fileTime.tm_mon) + '-' +
                  str(fileTime.tm_mday) + '-' +
                  str(fileTime.tm_hour) +
                  str(fileTime.tm_min) +  
                  str(fileTime.tm_sec))

            fileMsg.insert(index , fileElement)
            index += 1
            fileMsg.insert(index , strFileTime)
            allFileMsg.insert(allIndex , fileMsg)
            allIndex += 1

    return allFileMsg
    

def copyFile(fileMsgList):

#以二维序列为参数
#对文件执行复制重命名,删除
#重命名格式:'程序操作的顺序'+'原文件创建的时间'+'后缀'

    count = 0

    filePath = os.getcwd()

    nowTime = time.localtime(time.time())
    strNowTime = str(nowTime.tm_year) + str(nowTime.tm_mon) + str(nowTime.tm_mday)

    if not os.path.exists('newFolder-' + strNowTime):
        os.mkdir('newFolder-' + strNowTime)
        print("Create new folder, name is newFolder-" + strNowTime)
    
    else:
        print("Folder is exist,please rename a new folder")
        sys.exit()

    for fileElement in fileMsgList:

        print(fileElement)

        print('fileName:' + fileElement[0])

        print('fileTime:' + fileElement[1])


        newFileName = str(count) + '-' + fileElement[1] + '.png'
        fileObj = open(str(fileElement[0]), 'rb')
        
        fileObjContent = fileObj.read()        
        os.chdir('newFolder-' + strNowTime)
 
        newFileObj = open(newFileName, 'wb')
        newFileObj.write(fileObjContent)
        os.chdir(filePath)
        os.remove(fileElement[0])

        fileObj.close()
        newFileObj.close()

        count += 1
        
    print("The original file has been deleted")

    print("done")


    
if __name__ == '__main__':
    main()
