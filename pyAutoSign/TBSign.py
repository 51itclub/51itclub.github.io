#!/usr/bin/python2
#coding=utf-8

#
#   o丨Reborn <sbwtws@gmail.com>
#

import re
import time
import json
import urllib
import urllib2
import hashlib
#import threading
#from multiprocessing.pool import ThreadPool

COOKIE = {}
COOKIE['sbwtw_1'] = 'BDUSS=FtbUdUNEh1NlJtMVhTUUYtfnh3M25SWEk2emgtSGhVbkpObDUtd2hjQnBSYUJUQVFBQUFBJCQAAAAAAAAAAAEAAABv1WQwc2J3dHdfMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGm4eFNpuHhTSU;'
COOKIE['sbwtw_2'] = 'BDUSS=mRqem4tYlV0cVN2REdpYU9aNXlRb1RWdm5SODFkbGoyN25YSHpncGJhYWxSYUJUQVFBQUFBJCQAAAAAAAAAAAEAAAAU32Qwc2J3dHdfMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKW4eFOluHhTY;'
COOKIE['sbwtw_3'] = 'BDUSS=hmbmZRR2ZrMkRIbG10M0xTOEdWd1FkdTltckpzQ3VKNG93ZEVXMzZuek1SYUJUQVFBQUFBJCQAAAAAAAAAAAEAAABR5WQwc2J3dHdfMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMy4eFPMuHhTTj;'
COOKIE['sbwtw_4'] = 'BDUSS=GR4V3AyT0gtY0d4d3RJY1BLbnYxbU4yZVpTWEtvbENkYkQ0SUFaUFRIdnRSYUJUQVFBQUFBJCQAAAAAAAAAAAEAAACs6WQwc2J3dHdfNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO24eFPtuHhTZ;'
COOKIE['sbwtw_5'] = 'BDUSS=5Ob1prdX5kVHpPMTJsUDd4VnpvOEhIVFNNQzFhd2VUV1AybjBKLWhPOE9ScUJUQVFBQUFBJCQAAAAAAAAAAAEAAAB76mQwc2J3dHdfNQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA65eFMOuXhTck;'
COOKIE['sbwtw_6'] = 'BDUSS=JRSn5mTjVKVnptVWt0VGxMRlBzSmFyOWUxNXZCNDlmaVE4QmltZVR0OHNScUJUQVFBQUFBJCQAAAAAAAAAAAEAAADl8mQwc2J3dHdfNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACy5eFMsuXhTdG;'
COOKIE['sbwtw_7'] = 'BDUSS=Eh4TjR4Rmx0OEd3Y1RtZ0JISjBCdU81STNyWURHdkdBcnRnb1pEUWVEUk1ScUJUQVFBQUFBJCQAAAAAAAAAAAEAAACP9WQwc2J3dHdfNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEy5eFNMuXhTc;'
COOKIE['sbwtw_8'] = 'BDUSS=V1eENkdDh-NlN5RXkwM350NjBGV2RpOFdhbWxnQ2dkLUJpRklRb1FVbG5ScUJUQVFBQUFBJCQAAAAAAAAAAAEAAADP-mQwc2J3dHdfOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGe5eFNnuXhTeE;'

class TBSign():#threading.Thread):
    def __init__(self, userName, cookie):
        self.timeout = 5
        self.userName = userName
        self.cookie = cookie
        self.barList = []

        self.headers = {}
        self.headers['Host'] = 'tieba.baidu.com'
        self.headers['Referer'] = 'http://tieba.baidu.com/#'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cookie'] = cookie
        self.headers['User-Agent'] = 'Mozilla/5.0 (Linux; x86_64;) firefox 32.0 Gecko'

        #threading.Thread.__init__(self)

    def run(self):
        if not self.checkCookie():
            return None

        self.getBarList()
        
        for i in self.barList:
            try:
                self.sign(i)
            except:
                print self.userName, 'sign', i, 'Fail !'

    #sign
    def sign(self, barName):
        url = 'http://tieba.baidu.com/mo/m?kw=' + barName;
        res = self.httpPost(url)

        addr = re.search(r'<a\shref="([^"]+)">签到', res)

        if not addr:
            print self.userName, urllib.unquote(barName).decode('gbk').encode('utf-8'), 'already signed!'
            return None

        bduss = re.search(r'BDUSS=([^;]+);?', self.cookie)
        data = {}
        data['BDUSS'] = bduss.group(1)
        sign = 'BDUSS=' + data['BDUSS']
        data['_client_id'] = '04-00-DA-69-15-00-73-97-08-00-02-00-06-00-3C-43-01-00-34-F4-22-00-BC-35-19-01-5E-46'
        sign += '_client_id=' + data['_client_id']
        data['_client_type'] = '4'
        sign += '_client_type=' + data['_client_type']
        data['_client_version'] = '1.2.1.17'
        sign += '_client_version=' + data['_client_version']
        data['_phone_imei'] = '641b43b58d21b7a5814e1fd41b08e2a5'
        sign += '_phone_imei=' + data['_phone_imei']

        fid = re.search(r'fid"\svalue="(\w+)', res)
        data['fid'] = fid.group(1)
        sign += 'fid=' + data['fid']
        #data['kw'] = urllib.quote(urllib.unquote(barName).decode('gbk').encode('utf-8'))
        data['kw'] = urllib.unquote(barName).decode('gbk').encode('utf-8')
        sign += 'kw=' + data['kw']
        data['net_type'] = '3'
        sign += 'net_type=' + data['net_type']

        tbs = re.search(r'tbs"\svalue="(\w+)', res)
        data['tbs'] = tbs.group(1)
        sign += 'tbs=' + data['tbs']

        sign += 'tiebaclient!!!'
        data['sign'] = hashlib.md5(sign).hexdigest()

        url = 'http://c.tieba.baidu.com/c/c/forum/sign'
        res = self.toJson(self.httpPost(url, data))
        
        try:
            exp = res['user_info']['sign_bonus_point']
            print self.userName, 'sign', urllib.unquote(barName).decode('gbk').encode('utf-8'), 'successful, add exp', exp
        except:
            print self.userName, urllib.unquote(barName).decode('gbk').encode('utf-8'), res

    # get BarList
    def getBarList(self):
        page = 0
        while True:
            page += 1
            url = 'http://tieba.baidu.com/f/like/mylike?pn=' + str(page)
            res = self.httpPost(url)
            
            if not res:
                print self.userName, 'Find BarList Error'
                return None
        
            barList = re.findall(r'href="\/f\?kw=([^"]+)', res)

            if len(barList):
                self.barList += barList
            else:
                break

    # check cookie
    def checkCookie(self):
        url = 'http://tieba.baidu.com/dc/common/tbs'

        res = self.toJson(self.httpPost(url))

        if res['is_login']:
            self.tbs = res['tbs']
            return True
        else:
            print self.userName, 'Cookie Error'
            return None

    # post
    def httpPost(self, url, data = None):
        if data:
            data = urllib.urlencode(data)

        req = urllib2.Request(url, headers=self.headers)
        res = urllib2.urlopen(req, data, timeout = self.timeout)

        try:
            res = res.read()
        except:
            print self.userName, 'Http Post Error'
            return None

        return res

    # convert json
    def toJson(self, data):
        try:
            return json.loads(data)
        except:
            return None


for i in COOKIE:
    #threadPool.add()
    TBSign(i, COOKIE[i]).run()#.start()
