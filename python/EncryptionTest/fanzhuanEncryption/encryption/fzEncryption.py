print("反转加密法--加密");
while True:
    inputStr = input("输入要加密的内容('q' to Exit):")
    if inputStr == 'q' or 'Q':
        break
    elif inputStr != "":
        encryptionStr = ""
        i = len(inputStr) - 1
        while i >= 0:
            encryptionStr = encryptionStr + inputStr[i]
            i -= 1
        print("加密后得到:" + encryptionStr)
