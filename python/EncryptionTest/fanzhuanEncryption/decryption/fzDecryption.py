print("反转加密法--解密")
while True:
    inputStr = input("输入要解密的内容('q' to Exit):")
    if (inputStr == 'q') or (inputStr == 'Q'):
        break
    if inputStr != "":
        decryptionStr = ""
        i = len(inputStr) - 1
        while i >= 0:
            decryptionStr = decryptionStr + inputStr[i]
            i -= 1;
        print("解密后得到:" + decryptionStr)
