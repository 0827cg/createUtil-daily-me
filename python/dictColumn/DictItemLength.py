#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2018-06-22

from collections import OrderedDict

class DictItemLength():

    # 统计list集合中dict类型元素的长度
    # 将其想象成一个表格

    def __init__(self, listDictObj):

        self.listDictObj = listDictObj


    def getColumnMaxLength(self):

        # 获取单个列中所有元素的最长元素长度
        # self.listDictObj的长度就是列中的元素个数+1(包括列名)


        if(isinstance(self.listDictObj, list)):

            if(isinstance(self.listDictObj[0], dict)):


                dictResultObj = {}

                listKey = self.listDictObj[0].keys()
                print(listKey)

                for keyItem in listKey:

                    dictResultObj[keyItem] = len(keyItem)

                print(dictResultObj)

                for listDictItem in self.listDictObj:

                    print(type(listDictItem))

                    for listKeyItem in listKey:

                        if(len(str(listDictItem[listKeyItem])) > dictResultObj[listKeyItem]):
                            dictResultObj[listKeyItem] = len(str(listDictItem[listKeyItem]))



                        print([listDictItem[listKeyItem]])

                print(dictResultObj)
            else:
                print("子元素不符合")
        else:
            print("非list")

            # for intIndex in range(len(listKey)):
            #
            #     print(listDictItem[listKey(intIndex)])







orderDict = [OrderedDict([('columnName', 'append_user_id'), ('isNull', 'YES'), ('columnType', 'int(11)'), ('isKey', ''), ('columnComment', '')]),
             OrderedDict([('columnName', 'append_time'), ('isNull', 'YES'), ('columnType', 'int(11)'), ('isKey', ''), ('columnComment', '')]),
             OrderedDict([('columnName', 'modify_user_id'), ('isNull', 'YES'), ('columnType', 'int(11)'), ('isKey', ''),('columnComment', '')])]


listDict = [{'isNull': 'YES', 'columnName': 'append_user_id', 'columnComment': '', 'isKey': '', 'columnType': 'int(11)'},
            {'isNull': 'YES', 'columnName': 'append_time', 'columnComment': '', 'isKey': '', 'columnType': 'int(11)'},
            {'isNull': 'YES', 'columnName': 'modify_user_id', 'columnComment': '', 'isKey': '', 'columnType': 'int(11)'}]

listTest = ['1', '2', '3']



dictItemLengthObj = DictItemLength(listTest)
dictItemLengthObj.getColumnMaxLength()