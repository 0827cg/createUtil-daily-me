#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2018-08-14


# strContent = '| effect |YES |tinyint(1) | |是否逻辑删除
#             0、已被逻辑删除；1、未被逻辑删除 |'


def removeSpecialChar(strContent):

    strSplitContent = strContent.split('\n')

    print('strSplitContent: ', strSplitContent)
    strNewContent = ''.join(strSplitContent)
    print('strNewContent: ', strNewContent)

def replaceString(strContent):

    arrNeedReplace = {'\t': ' ', '\n': ' '}

    # for intIndex in range(len(arrNeedReplace)):
    #     strContent.replace(item, ' ')

    for itemOld, itemNew in arrNeedReplace.items():
        strContent = strContent.replace(itemOld, itemNew)


    print('strNewContent: ' + strContent)


strContent = 'tes t\tdgsng\ntset'
print(strContent)
replaceString(strContent)


