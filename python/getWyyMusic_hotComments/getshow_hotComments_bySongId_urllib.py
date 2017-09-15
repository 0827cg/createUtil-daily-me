import urllib.request
import json


def main():
    song_id='210281'
    hotComments_dict = get_comments_dict(song_id)
    list_msg_dict(hotComments_dict)


def get_comments_dict(song_id):

    url = url = (' https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s') % (song_id)

    headers = {}
    headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' +
                              '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Referer'] = 'http://music.163.com/'
    headers['Accept'] = '*/*'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    user_data = {}
    user_data['params'] = ('Wu2sOFQ+X+6RY50DLGM+pV5SesERq6X/kOo5xbdwDnvF/l1J7H8' +
                           'HOaqXcJjodzHomcP0LfLD9NOdiWywv62TRjI7Eab9BPTNn34GdysVVs2i10BB' +
                           'zhFiF3bhxp4XH9NNjb9MJ3kwn7IRMTmLV91VoZFFCEaiSU2h7ErBRjoAJIN6vP' +
                           'NuHCztXhc5z5dXNY2/ZreCUtxLzGfzGSGJzknCH6ykYXkh4Xx2k2B8IMNp+i0=')
    user_data['encSecKey'] = ('c844dd16d0e1ab330ae99f0d6948951eeb1effed034222098dcc5' +
                              '58ed6bdcd469475ff7f7f3f1c1a3577cb538a95872fb03f10c30a6578ec488' +
                              '61152c3ceb2ab338d1967145577eb9375b6cd42217f265460aa8374b46e5' +
                              '6a1120fa83056ea791eaccbd8f74fee3efe42ed03d99b1ac0574607e59520f4' +
                              '225f38e5132606c3fd')

    data = urllib.parse.urlencode(user_data).encode("utf-8")
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    response_text = response.read().decode('utf-8')
    response_text_dict = json.loads(response_text)
    #print(response_text)
    return response_text_dict

def list_msg_dict(data_dict):
    #打印hotComments中的content,nickname,likedCount
    #即打印热评内容，用户名，点赞数量
    if isinstance(data_dict, dict):
        for i in range(len(data_dict['hotComments'])):
            print(data_dict['hotComments'][i]['content'])
            print("\t\t---" + data_dict['hotComments'][i]['user']['nickname'] +
                  "<" + str(data_dict['hotComments'][i]['likedCount']) + ">Liked" + "\n")



if __name__ == '__main__':
    main()
