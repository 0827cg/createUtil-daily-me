print("凯撒加密算法--加密")

key = 13
strLetter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

while True:
    
    encryptionStr = ""
    
    inputStr = input("输入要加密的内容('q' to Exit):")
    if (inputStr == 'q') or (inputStr == 'Q'):
        break
    elif inputStr != "":
        inputStr = inputStr.upper()
        for i in inputStr:
            if i in strLetter:
                num = strLetter.find(i)
                num += key
                if num >= len(strLetter):
                    num -= len(strLetter)
                elif num < 0:
                    num += len(strLetter)
                encryptionStr += strLetter[num]
            else:
                encryptionStr += i
            
        print("加密后得到:" + encryptionStr)
