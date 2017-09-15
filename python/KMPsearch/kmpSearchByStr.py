import re
import os
import sys
import time
import chardet

#describe: find files by string, use kmp algorithm
#author: cg

def main():

    print("查找出该路径下所有包含此字符串的文件路径")
    while True:
        print("请输入文件路径('q to exit') :")
        inputFilePath = input('>')
        if (inputFilePath == 'q') or (inputFilePath == 'Q'):
            break
        elif inputFilePath != "":
            if os.path.exists(inputFilePath):
                print("请输入要查找的字符串 :")
                inputStr = input('>')
                if (inputStr == 'q') or (inputStr == 'Q'):
                    break
                startTime = time.time()
                kmpTable = getKMPtable("inputStr")
                resultList = searchStr(inputStr, inputFilePath, kmpTable)
                useTime = round((time.time() - startTime), 4)
                showResult(resultList)
                print("查找所耗时间 %s s" %useTime)
                print("<-----查找完成----->")
                print('')
            else:
                print("文件路径[%s]不存在" %(inputFilePath))
                continue

    
    #kmpTable = getKMPtable("ABCDABD")
    #kmpSearchStrByStr("BBC ABCDAB ABCDABCDABDE", "ABCDABD", kmpTable)

def searchStr(strSearch, path, kmpTable):
    listTotalFile = []
    dictTotalMsg = {}
    totalFile = 0
    for rootPathStr, dirNameLists, fileNameLists in os.walk(path, True):
        for fileName in fileNameLists:
            filePath = os.path.join(rootPathStr, fileName)
            fileEncoding = getFileEncode(filePath)
            with open(filePath, 'r', encoding=fileEncoding) as fileObj:
                totalNum = 0
                lineNum = 0
                dictTotal = {}
                listItemLine = []
                listItemCount = []
                while True:
                    try:
                        line = fileObj.readline()
                        lineNum += 1
                        if line:
                            #resultList = re.findall(strSearch, line)
                            existCount = kmpSearchStrByStr(line, strSearch, kmpTable)
                            if existCount > 0:
                                totalNum += existCount
                                listItemLine.append(lineNum)
                                listItemCount.append(existCount)
                        else:
                            break
                    except Exception:
                        print("error:")
                        print("<<" + filePath + "读取失败 >>")
                        continue

                if totalNum > 0:
                    dictTotal['filePath'] = filePath
                    dictTotal['totalCount'] = totalNum
                    dictTotal['detailLine'] = listItemLine
                    dictTotal['detailCount'] = listItemCount
                    listTotalFile.append(dictTotal)
        totalFile += (len(fileNameLists))
    dictTotalMsg['findPath'] = path
    dictTotalMsg['findStr'] = strSearch
    dictTotalMsg['totalFileNum'] = totalFile
    dictTotalMsg['msg'] = listTotalFile
    return dictTotalMsg


def getFileEncode(filePath):
    with open(filePath, 'rb') as fileObj:
        data = fileObj.read()
        fileDataDict = chardet.detect(data)
        return fileDataDict.get('encoding')
    
def showResult(dictTotalMsg):
    listMsg = dictTotalMsg.get('msg')
    print("<-----查找结果----->")
    print("查找路径为: %s" %(dictTotalMsg.get('findPath')))
    print("查找的字符串为: %s" %(dictTotalMsg.get('findStr')))
    if len(listMsg) > 0:
        print("包含该字符串的文件路径及详情如下 :")
    else:
        print("抱歉 , 未查找到相应文件")
    for i in range(len(listMsg)):
        print("文件%s路径 : %s" %((i + 1), listMsg[i].get('filePath')))
        print("出现该字符串的总数 : %s" %(listMsg[i].get('totalCount')))
        print("出现该字符串的行数 : %s" %(listMsg[i].get('detailLine')))
        print("行数对应的出现次数 : %s" %(listMsg[i].get('detailCount')))
    print("总查找文件个数 : %s" %(dictTotalMsg.get('totalFileNum')))


def kmpSearchStrByStr(totalStr, strSearch, kmpTable):

    #kmp算法查找
    #返回字符串中包含搜索串的个数

    listSearch = list(strSearch)
    listTotal = list(totalStr)
    
    s = 0
    t = 0
    existCount = 0
    while((s < len(listSearch)) & (t < len(listTotal))):
        if(listSearch[s] == listTotal[t]):
            if((s + 1) != len(listSearch)):
                s+=1
                t+=1
            else:
                existCount+=1
                if((len(listTotal) - (t + 1)) >= len(listSearch)):
                    s = 0
                    t+=1
                else:
                    break;
        elif(s == 0):
            s = 0
            t+=1
        else:
            s = s - (s - kmpTable[(s - 1)])
        if((t + 1) >= len(listTotal)):
            break
    #print(existCount)
    return existCount
    


def getKMPtable(strSearch):

    #获取kmp的部分匹配数值表
    #但得先获取字符串所有可能长度的最大公告元素长度，将其存放到int数组中返回

    intTablesLength = len(strSearch)
    kmpTable = []

    for i in range(intTablesLength):
        strItem = strSearch[0 : i + 1]
        intMaxPublicNum = getMaxPublicNum(strItem)
        kmpTable.append(intMaxPublicNum)

    #print(kmpTable)
    return kmpTable


def getMaxPublicNum(strItem):

    #获取前缀和后缀，并最终对比得到最大的公共元素长度,并返回
    
    intMaxPublicNum = 0
    intItemLength = len(strItem)

    listFront = []
    listBack = []

    for i in range(intItemLength - 1):
        listFront.append(strItem[0 : i + 1])

    for i in range(intItemLength, 1, -1):
        listBack.append(strItem[i - 1 : intItemLength])

    n = -1
    for i in range(intItemLength - 1):
        if(listFront[i] == listBack[i]):
            n = i
    if(n != -1):
        intMaxPublicNum = len(listFront[n])
        
    #print(intMaxPublicNum)
    return intMaxPublicNum


if __name__ == '__main__':
    main()
