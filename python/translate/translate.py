import urllib.request
import urllib.parse
import json

while True:

    inputStr = input("输入要翻译的内容('q' to Exit):")

    if (inputStr == 'q') or (inputStr == 'Q'):
        break
    elif inputStr != "":
        
        url = ('http://fanyi.youdao.com/translate?' +
        'smartresult=dict&smartresult=rule&' +
        'smartresult=ugc&sessionFrom=dict2.' +
        'indexhttp://fanyi.youdao.com/translate?' +
        'smartresult=dict&smartresult=rule&' +
        'smartresult=ugc&sessionFrom=dict2.index')

        head = {}
        head['Uset-Agent'] = ('Mozilla/5.0 (X11;' +
        'Linux x86_64) AppleWebKit/537.36 (KHTML,' +
        'like Gecko) Chrome/54.0.2840.100 Safari/' +
        '537.36')

        data = {}
        data['type'] = 'AUTO'
        data['i'] = inputStr
        data['doctype'] = 'json'
        data['xmlVersion'] = '1.8'
        data['keyfrom'] = 'fanyi.web'
        data['ue'] = 'UTF-8'
        data['action'] = 'FY_BY_CLICKBUTTON'
        data['typoResult'] = 'true'
        data = urllib.parse.urlencode(data).encode('utf-8')

        req = urllib.request.Request(url, data, head)
        reponse = urllib.request.urlopen(req)
        html = reponse.read().decode('utf-8')

        msg = json.loads(html)
        translateResultStr = msg['translateResult'][0][0]['tgt']
        print(translateResultStr)

        if 'smartResult' in msg:
            smartEntriesResultStr = msg['smartResult']['entries']
            for index in smartEntriesResultStr:
                if index != "":
                    print(index)
        else:
             print("Input Error")
