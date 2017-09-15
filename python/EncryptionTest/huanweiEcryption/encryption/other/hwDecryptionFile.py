import time
import os
import sys
import math

def main():

    print("解密同目录下被encryptionFile.py加密的ShowFile-enctypted.txt文件")
    inputFileName = 'ShowFile-encrypted.java'
    outputFileName = 'ShowFile-decrypted.java'
    key = 8
    
    if not os.path.exists(inputFileName):
        print("%s 不存在" %(inputFileName))
        sys.exit()

    if os.path.exists(outputFileName):
        print("This will overwrite the file %s.(c)Continue or (q)Quit ?" %(outputFileName))
        choiceStr = input('> ')
        if not choiceStr.lower().startswith('c'):
            sys.exit()
    
    #读取被加密文件的内容
    fileContent = readFileContent(inputFileName)
    
    firstStartTime = time.time()
    #解密文件内容
    decryptionFileContent = decryptionStr(key,fileContent)
    
    #将解密后的内容中的'|'替换成'\n'
    normalFileContent = regetNewLineSymbol(decryptionFileContent)
    decryptionTime = round((time.time() - firstStartTime), 4)

    #将解密得到的内容写到新的文件
    writeFileContent(outputFileName,normalFileContent)
    totalTime = round((time.time() - firstStartTime), 4)

    print("Done decryption %s (%s characters)" %(inputFileName,len(normalFileContent)))
    print("encrypted file is %s" %outputFileName)
    print("enctyption time: %s seconds" %decryptionTime)
    print("TotalTime %s seconds" %totalTime)


def readFileContent(inputFileName):

    #读取文件内容并返回
    
    fileObj = open(inputFileName, 'r')
    fileContent = fileObj.read()
    fileObj.close()
    return fileContent

def writeFileContent(outputFileName,fileContent):
    fileObj = open(outputFileName,'w')
    fileObj.write(fileContent)
    fileObj.close()

def decryptionStr(intKey,strContent):
    
    #intKey:换位加密算法秘钥-用来解密
    #strContent:需要解密的内容(且不包含换行符)
    #解密后返回

    numOfCol = math.ceil(len(strContent) / intKey)

    numOfRow = intKey

    numOfShadedBox = (numOfCol * numOfRow) - len(strContent)

    decryptionStr = [''] * numOfCol

    pointerCol = 0
    pointerRow = 0

    for element in strContent:
        decryptionStr[pointerCol] += element
        pointerCol += 1

        if(pointerCol == numOfCol) or ((pointerCol == numOfCol - 1) and (pointerRow >= numOfRow - numOfShadedBox)):
            pointerCol = 0
            pointerRow += 1
            
    return ''.join(decryptionStr)
    
    
            
def regetNewLineSymbol(strContent):

    #将含有'|'符号的内容还原成有'\n'的,并返回
    
    reStrContent = strContent.replace("|","\n")
    return reStrContent


if __name__ == '__main__':
    main()
