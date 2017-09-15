print("反转加密法")
while True:
    strChoice = input("选择1.加密 2.解密('q' to Exit):")
    if strChoice == '1':
        inputStr = input("输入要加密的内容('q' to Exit):")
        if (inputStr == 'q') or (inputStr == 'Q'):
            break
        elif inputStr == 'b':
            continue
        elif inputStr != "":
            encryptionStr = ""
            i = len(inputStr) - 1
            while i >= 0:
                encryptionStr = encryptionStr + inputStr[i]
                i -= 1
            print("加密后得到:" + encryptionStr)
    elif strChoice == '2':
        inputStr = input("输入要解密的内容('q' to Exit):")
        if (inputStr == 'q') or (inputStr == 'Q'):
            break
        elif (inputStr == 'b') or (inputStr == 'B'):
            continue
        elif inputStr != "":
            decryptionStr = ""
            i = len(inputStr) - 1
            while i >= 0:
                decryptionStr = decryptionStr + inputStr[i]
                i -= 1
            print("解密后得到:" + decryptionStr)
    elif strChoice == 'q':
        break
    else:
        print("Input Error")

