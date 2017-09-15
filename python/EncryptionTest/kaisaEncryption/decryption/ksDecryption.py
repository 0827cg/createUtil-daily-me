print("凯撒加密算法--解密")
key = 13
strLetter = 'abcdefghijklmnopqrstuvwxyz'

while True:
    decryption = ""
    inputStr = input("输入要解密的内容('q' to Exit):")
    if (inputStr == 'q') or (inputStr == 'Q'):
        break
    elif inputStr != "":
        inputStr = inputStr.lower()
        for i in inputStr:
            if i in strLetter:
                num = strLetter.find(i)
                num -= key
                if num >= len(strLetter):
                    num -= len(strLetter)
                elif num < 0:
                    num += len(strLetter)
                decryption += strLetter[num]
            else:
                decryption += i
        print("解密后得到:" + decryption)
    
