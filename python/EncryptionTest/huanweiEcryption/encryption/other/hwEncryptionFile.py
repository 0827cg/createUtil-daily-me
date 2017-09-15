import time
import os
import sys

def main():
    
    print("使用换位算法加密同目录下的ShowFile.java文件")
    inputFileName = 'ShowFile.java'
    outputFileName = 'ShowFile-encrypted.java'
    key = 8
    
    if not os.path.exists(inputFileName):
        print("%s 不存在" %(inputFileName))
        sys.exit()

    if os.path.exists(outputFileName):
        print("This will overwrite the file %s.(c)Continue or (q)Quit ?" %(outputFileName))
        choiceStr = input('> ')
        if not choiceStr.lower().startswith('c'):
            sys.exit()

    #读取文件内容,并将'\n'替换成'|'        
    fileContent = readFile(inputFileName)
    
    firstStartTime = time.time()

    #将内容加密
    encryptionFileContent = encryptionStr(key,fileContent)
    
    encryptionTime = round((time.time() - firstStartTime), 4) 

    #将加密后的内容写入到新的文件中
    writeFile(outputFileName,encryptionFileContent)

    totalTime = round((time.time() - firstStartTime), 4)
    print("Done encryption %s (%s characters)" %(inputFileName,len(encryptionFileContent)))
    print("encrypted file is %s" %outputFileName)
    print("enctyption time: %s seconds" %encryptionTime)
    print("TotalTime %s seconds" %totalTime)

def readFile(inputFileName):
    
    #读取文件内容,先将换行符替换成'|',再全部返回
    
    fileContent = ""
    fileObj = open(inputFileName, 'r')
    while True:
        line = fileObj.readline()
        if line:
            line = line.replace("\n","|")
            fileContent += line
        else:
            break
    fileObj.close()

    return fileContent

def encryptionStr(intKey,strContent):

    #intKey:换位加密算法秘钥
    #strContent:需要加密的内容(且不包含换行符)
    #加密后返回

    encryptionStrContent = [''] * intKey
    for colNum in range(intKey):
        pointer = colNum
        while pointer < len(strContent):
            encryptionStrContent[colNum] += strContent[pointer]
            pointer += intKey

    return ''.join(encryptionStrContent)

def writeFile(outputFileName,fileContent):
    fileObj = open(outputFileName,'w')
    fileObj.write(fileContent)
    fileObj.close()
    

if __name__ == '__main__':
    main()
