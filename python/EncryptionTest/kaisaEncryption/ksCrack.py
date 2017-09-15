print("破解凯撒加密算法(如果字母不变)")
cryptionStr = "GUVF VF ZL FRPERG ZRFFNTR"
decryptionStr = "this is my secret message"
strLetter = 'abcdefghijklmnopqrstuvwxyz'
cryptionStr = cryptionStr.lower()
key = 0
while key < 26:
    produceStr = ""
    for i in cryptionStr:
        if i in strLetter:
            num = strLetter.find(i)
            num -= key
            if num >= len(strLetter):
                num -= len(strLetter)
            elif num < 0:
                num += len(strLetter)
            produceStr += strLetter[num]
        else:
            produceStr += i
    if produceStr == decryptionStr:
        print("破解成功,key = %s" %key)
        break
    key += 1
    if key == 25:
        print("破解失败")
