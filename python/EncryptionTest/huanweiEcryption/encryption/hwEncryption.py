#换位加密算法的秘钥大小被限制为要小于加密消息长度的一半
#消息越长可以用来加密它的秘钥就越多

def main():
    print("换位加密算法--加密")
    key = 8
    while True:
        
        inputStr = input("输入要加密的内容('q' to Exit):")
        if (inputStr == 'q') or (inputStr == 'Q'):
            break
        elif inputStr != "":
            encryptionStr = produceEncryptionStr(key,inputStr)
            
            print("加密后得到:" + encryptionStr)


def produceEncryptionStr(key,inputStr):
    encryptionStr = [''] * key
    for colNum in range(key):
        pointerNum = colNum
        while pointerNum < len(inputStr):
            encryptionStr[colNum] += inputStr[pointerNum]
            pointerNum += key
    return ''.join(encryptionStr)


if __name__ == '__main__':
    main()

