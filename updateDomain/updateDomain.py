#!/usr/bin/python
# -*- coding: gbk -*-
"""
-------------------------------------------------------------------------------
【版本信息】
版本：     v1.0
作者：     crifan

【详细信息】
用于：
【教程】抓取网并网页中所需要的信息 之 Python版
http://www.crifan.com/crawl_website_html_and_extract_info_using_python/
的示例代码。

-------------------------------------------------------------------------------
"""

#---------------------------------import---------------------------------------
#import urllib;
import urllib2;
from urllib2 import Request, urlopen, URLError, HTTPError
import re;
from BeautifulSoup import BeautifulSoup;
from urlparse import *
import sys, socket
#import dns.resolver
#import DNS
#------------------------------------------------------------------------------

#git clone https://github.com/rthalley/dnspython.git
#cd dnspython
#python setup.py install


def getIPAddFromFile(fobj):
    regex = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', re.IGNORECASE)
    ipadds = re.findall(regex, fobj)
    print ipadds
    return ipadds

def getPhoneNumFromFile(fobj):
    regex = re.compile(r'1\d{10}', re.IGNORECASE)
    phonenums = re.findall(regex, fobj)
    print phonenums
    return phonenums

def getMailAddFromFile(fobj):
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)
    mails = re.findall(regex, fobj)
    print mails
    return mails

def getUrlFromFile(fobj):
    regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
    urls = regex.findall(fobj)
    print urls
    return urls

def main1(FilefilePath):
    fobj = open(FilefilePath, 'rb').read()
    urllist = getUrlFromFile(fobj)
    mailList = getMailAddFromFile(fobj)
    phoneNum = getPhoneNumFromFile(fobj)
    ipaddlist = getIPAddFromFile(fobj)

def www_ip(name):  #域名转IP
    try:
        result = socket.getaddrinfo(name, None)
        return result[0][4][0]
    except:
        return 0

def ip_port(ip):  #查看IP端口是否开放
    port=21
    s=socket.socket()
    #address="127.0.0.1"
    try:
        s.connect((ip,port))
        #print 'IP:',ip,"port:",port,"以开放"
        return 1
    except socket.error,e:
        #print 'IP:',ip,"port:",port,"未开放"
        return 0


def main():
    #userMainUrl = "http://www.songtaste.com/user/351979/";
    #userMainUrl = "http://47tata.com/";
    #req = urllib2.Request(userMainUrl);
    #resp = urllib2.urlopen(req);
    #respHtml = resp.read();
    #print "respHtml=",respHtml; # you should see the ouput html

    #print "Method 1: Use python re to extract info from html";
    #<h1 class="h1user">crifan</h1>
    #foundH1user = re.search('<h1\s+?class="h1user">(?P<h1user>.+?)</h1>', respHtml);
    #print "foundH1user=",foundH1user;
    #if(foundH1user):
    #    h1user = foundH1user.group("h1user");
    #    print "h1user=",h1user;

    #print "Method 2: Use python third lib BeautifulSoup to extract info from html";
    #songtasteHtmlEncoding = "GB2312";
    #soup = BeautifulSoup(respHtml, fromEncoding=songtasteHtmlEncoding);
    #<h1 class="h1user">crifan</h1>
    #foundClassH1user = soup.find(attrs={"class":"h1user"});
    #print "foundClassH1user=%s",foundClassH1user;
    #if(foundClassH1user):
    #    h1userStr = foundClassH1user.string;
    #    print "h1userStr=",h1userStr;

    www= "47tata.com"
    IP=www_ip(www)
    if IP:
        pass
        #print www,"ip地址：",IP
        #if ip_port(IP):
        #    print IP,"开放21端口"
        #else:
        #    print IP,"未开21放端口"
    else:
        print www,"域名转IP失败"

    #print socket.gethostbyname('47tata.com') #获取域名对应的IP
    #print socket.gethostbyname(socket.gethostname()) #获取主机名
    #print socket.gethostbyname_ex(socket.gethostname()) #根据主机名判断出IP
    #print socket.gethostbyname_ex('47tata.com')

    www= "44bpbp.com"
    IP=www_ip(www)
    #newhost=socket.gethostbyaddr(IP)
    #print www,"ip地址：",IP,"新域名:",newhost


    #my_resolver = dns.resolver.Resolver()
    # 这里换成你指定的某一个域名服务器的ip
    #my_resolver.nameservers = ['8.8.8.8']
    # 需要查询的域名
    #answer = my_resolver.query('www.xuli.co')
    #print answer.response
    #print DNS.revlookup("192.189.54.17")

    www= "47tata.com"
    www='695p.com'
    www='889rr.com'
    www='66riri.com'
    www='44bfbf.com'
    www='z587.com'
    www='44bpbp.com'
    www='207r.com'
    www='207z.com'
    www='206d.com'
    www='202z.com'
    www='02ppp.com'
    www='1.695n.com'


    http://44tktk.com/
    print www_ip(www)

    try:
        print socket.gethostbyaddr(www_ip(www))
    except ValueError, e:
        print e
    except HTTPError, e:
        print e.code
        print e.read()
    except URLError, e:
        print e.reason
    except socket.herror, e:
        print "Couldn't look up name:", e
        sys.exc_clear()
    except Exception: 
        sys.exc_clear()


    try:
        request = urllib2.Request(www)        
        content = urllib2.urlopen(request)
        #location = content.info()
        #print location
        print content.geturl()
        #print content.read()
    except ValueError, e:
        print e
    except HTTPError, e:
        print e.code
        print e.read()
    except URLError, e:
        print e.reason
    except socket.herror, e:
        print "Couldn't look up name:", e
        sys.exc_clear()
    except Exception: 
        sys.exc_clear()


    try:
        print urllib2.urlopen(urllib2.Request(www)).read()
    except ValueError, e:
        print e
    except HTTPError, e:
        print e.code
        print e.read()
    except URLError, e:
        print e.reason
    except socket.herror, e:
        print "Couldn't look up name:", e
        sys.exc_clear()
    except Exception: 
        sys.exc_clear()

    #host=raw_input('host:')
    #result=socket.getaddrinfo(www,None)
    #counter=0
    #for i in result:
    #    print "%-2d:%s"%(counter,i[4])
    #    counter+=1

    #url = 'http://segmentfault.com/blog/biu/1190000000330941'
    #r = urlparse(url)
    #print r.netloc
    #print "respHtml=",respHtml;
    return


#try:
#    result = socket.gethostbyaddr('45.34.54.39')
#    print 'Primary hostname:'
#    print ' ' + result[0] # Display the list of available addresses that is also returned
#    print '\nAddresses:'
#    for item in result[2]:
#        print ' ' + item
#except socket.herror, e:
#    print "Couldn't look up name:", e



###############################################################################
if __name__=="__main__":
    main();






















