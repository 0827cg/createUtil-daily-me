import math

def main():
    print("换位加密算法--解密")
    key = 8
    while True:
        inputStr = input("输入要解密的内容('q' to Exit):")
        if (inputStr == 'q') or (inputStr == 'Q'):
            break
        elif inputStr != "":
            decryptionStr = produceDecryptionStr(key,inputStr)
            print("解密后得到:" + decryptionStr)
            

def produceDecryptionStr(key,inputStr):
    colNum = math.ceil(len(inputStr) / key)
    rowNum = key
    unUseBoxNum = colNum * rowNum - len(inputStr)
    decryptionStr = [''] * colNum

    colPointer = 0
    rowPointer = 0

    for element in inputStr:
        decryptionStr[colPointer] += element
        colPointer += 1

        if (colPointer == colNum) or ((colPointer == colNum - 1) and (rowPointer >= rowNum - unUseBoxNum)):
            colPointer = 0
            rowPointer += 1
    return ''.join(decryptionStr)

if __name__ == '__main__':
    main()
