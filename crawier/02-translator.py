import requests
import time
import random
import hashlib


class YoudaoTranslate:
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/\
                           535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
                          'Referer': 'http://fanyi.youdao.com/',
                          'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
        }
        self.data = {
            'i': None,
            'client': 'fanyideskweb',
            'keyfrom': 'fanyi.web',
            'salt': None,
            'sign': None
        }
        self.word = input("原文：")
    def request(self):
        self.data['i'] = self.word
        self.data['salt'] = str(time.time()*1000 + random.randint(1, 10))
        sign = 'fanyideskweb' + self.word + self.data['salt'] + '6x(ZHw]mwzX#u0V7@yfwK'
        self.data['sign'] = hashlib.md5(sign.encode('utf-8')).hexdigest()
        html = requests.post(self.url, data=self.data, headers=self.user_agent)
        j = html.json()['translateResult']
        return j[0]


if __name__ == '__main__':
    fanyi = YoudaoTranslate()
    a = fanyi.request()
    print('译文：'+a)
