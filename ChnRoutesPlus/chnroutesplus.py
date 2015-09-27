#!/usr/bin/env python
# -*- coding: gbk -*-
#coding=gbk

#Modified by 51itclub,welcome to my site:51itclub.net
#----------------------------------------------------------------------

test=0
day=7
metric=5
ng=''




#----------------------------------------------------------------------


import re
import urllib2
import sys
import argparse
import math
import textwrap
import datetime
import os
import platform



n=0
results=[]
if os.path.exists('test.txt'):
    open('test.txt','a').close
    timestamp=os.path.getmtime('test.txt')
    date = datetime.datetime.fromtimestamp(timestamp)
    nw = datetime.datetime.now()
    #print ' 最后修改时间为: ',date.strftime('%Y-%m-%d %H:%M:%S')
    #print date.year,date.month,date.day
    #print nw.year,nw.month,nw.day
    d1=datetime.datetime(nw.year,nw.month,nw.day)
    d2=datetime.datetime(date.year,date.month,date.day)
    #print (d1-d2).days
    d3=(d1-d2).days
else:
    d3=8
    day=0
sysstr = platform.system()
#print platform.version()


import socket
import struct


import pkgutil
import urlparse
import json
import logging
import copy

gfwlist_url = 'https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt' # ban with gfw, you need proxy to access
gfwlist_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                      help='path to gfwlist', metavar='GFWLIST')
    parser.add_argument('-f', '--file', dest='output', required=True,
                      help='path to output pac', metavar='PAC')
    parser.add_argument('-p', '--proxy', dest='proxy', required=True,
                        help='the proxy parameter in the pac file, for example,\
                        "SOCKS5 127.0.0.1:1080;"', metavar='PROXY')
    parser.add_argument('--user-rule', dest='user_rule',
                        help='user rule file, which will be appended to gfwlist')
    return parser.parse_args()


def decode_gfwlist(content):
    # decode base64 if have to
    try:
        if '.' in content:
            raise
        return content.decode('base64')
    except:
        return content


def get_hostname(something):
    try:
        # quite enough for GFW
        if not something.startswith('http:'):
            something = 'http://' + something
        r = urlparse.urlparse(something)
        return r.hostname
    except Exception as e:
        logging.error(e)
        return None


def add_domain_to_set(s, something):
    hostname = get_hostname(something)
    if hostname is not None:
        if hostname.startswith('.'):
            hostname = hostname.lstrip('.')
        if hostname.endswith('/'):
            hostname = hostname.rstrip('/')
        if hostname:
            s.add(hostname)


def parse_gfwlist(content, user_rule=None):
    builtin_rules = pkgutil.get_data('gfwlist2pacplus', 'resources/builtin.txt').splitlines(False)
    gfwlist = content.splitlines(False)
    if user_rule:
        gfwlist.extend(user_rule.splitlines(False))
    domains = set(builtin_rules)
    for line in gfwlist:
        if line.find('.*') >= 0:
            continue
        elif line.find('*') >= 0:
            line = line.replace('*', '/')
        if line.startswith('!'):
            continue
        elif line.startswith('['):
            continue
        elif line.startswith('@'):
            # ignore white list
            continue
        elif line.startswith('||'):
            add_domain_to_set(domains, line.lstrip('||'))
        elif line.startswith('|'):
            add_domain_to_set(domains, line.lstrip('|'))
        elif line.startswith('.'):
            add_domain_to_set(domains, line.lstrip('.'))
        else:
            add_domain_to_set(domains, line)
    return domains

def reduce_domains(domains):
    # reduce 'www.google.com' to 'google.com'
    # remove invalid domains
    tld_content = pkgutil.get_data('gfwlist2pacplus', 'resources/tld.txt')
    tlds = set(tld_content.splitlines(False))
    cus_content = pkgutil.get_data('gfwlist2pacplus', 'resources/custom.txt')
    cuss = cus_content.splitlines(False)
    ban_content = pkgutil.get_data('gfwlist2pacplus', 'resources/ban.txt')
    bans = set(ban_content.splitlines(False))
    new_domains = set()
    for cus in cuss:
        new_domains.add(cus)
    for domain in domains:
        domain_parts = domain.split('.')
        last_root_domain = None
        for i in xrange(0, len(domain_parts)):
            root_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            if i == 0:
                if not tlds.__contains__(root_domain):
                    # root_domain is not a valid tld
                    break
            last_root_domain = root_domain
            if tlds.__contains__(root_domain):
                continue
            else:
                break
        if last_root_domain is not None \
            and last_root_domain not in bans \
            and last_root_domain not in new_domains:
            same = False
            for cus in new_domains:
                if len(cus) < len(last_root_domain):
                    if cmp(cus[::-1] + '.', last_root_domain[::-1][0:len(cus)+1]) == 0 :
                        same = True
                        break
                elif len(cus) > len(last_root_domain):
                    if cmp(last_root_domain[::-1] + '.', cus[::-1][0:len(last_root_domain)+1]) == 0 :
                        new_domains.remove(cus)
                        break
            if not same :
                new_domains.add(last_root_domain)
    return new_domains











def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


def generate_pac(proxy):
    global d3,day,results
    if d3<day:return

    results  = fetch_ip_data_leask()
    pacfile  = 'proxy.pac'
    rfile    = open(pacfile, 'w')
    results.insert(0, (ip2long('127.0.0.1'),   ip2long('255.0.0.0'),   0))
    results.insert(1, (ip2long('10.0.0.0'),    ip2long('255.0.0.0'),   0))
    results.insert(2, (ip2long('172.16.0.0'),  ip2long('255.240.0.0'), 0))
    results.insert(3, (ip2long('192.168.0.0'), ip2long('255.255.0.0'), 0))

    def ip(item):
        return item[0]

    results = sorted(results, key = ip)

    if os.path.exists('gfwlist.txt'):
        content = open('gfwlist.txt').read()
    elif os.path.exists('wget.exe') and sysstr =="Windows":
        print 'Downloading gfwlist from %s' % gfwlist_url
        os.system("wget --no-check-certificate -c "+gfwlist_url+" -O gfwlist.txt")
        content = open('gfwlist.txt').read()
    else:
        print 'Downloading gfwlist from %s' % gfwlist_url
        content = urllib2.urlopen(gfwlist_url, timeout=10).read()
    content = decode_gfwlist(content)
    domains = parse_gfwlist(content)
    domains = reduce_domains(domains)
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = 1
    proxy_content = json.dumps(domains_dict, indent=2)
    #print proxy_content


    strLines = """\
//    http://dwz.cn/1N9nW7
//IPV4 TO IPV6:http://www.subnetonline.com/pages/subnet-calculators/ipv4-to-ipv6-converter.php
//IPV6地址加端口表示方法http://desert3.iteye.com/blog/1595253

//-----------------------------------------------------------------
var hasOwnProperty = Object.hasOwnProperty;
var extend=function(o,n,override){for(var p in n)if(n.hasOwnProperty(p) && (!o.hasOwnProperty(p) || override))o[p]=n[p];for(var p in o)n[p]=o[p]};

var direct = "DIRECT";
var wall_proxy = function(){ return "__PROXY__;%s"; };
var wall_v6_proxy = function(){ return "PROXY [fe80::c0a8:201]:8118;PROXY [fe80::c0a8:201]:8087;PROXY [0::7f00:1]:8087;PROXY [0::7f00:1]:8118;SOCKS5 [fe80::c0a8:201]:1080;SOCKS5 [0::7f00:1]:1080;SOCKS5 [0::7f00:1]:48102;SOCKS5 [0::7f00:1]:65500;SOCKS5 [0::7f00:1]:7070;" + direct; };
var ip_proxy = function(){ return wall_proxy(); };
var ipv6_proxy = function(){ return wall_v6_proxy(); };
var nowall_proxy = function(){ return direct; };
var block = function(){ return "PROXY 127.0.0.1:8086"; };
var autoproxy = 'PROXY 127.0.0.1:8087';
var blackhole = block();
var autoproxy = wall_proxy();
var defaultproxy = direct
//var wall_proxy = function(){ return direct+";__PROXY__;PROXY 192.168.2.1:8118;PROXY 127.0.0.1:8118;SOCKS5 127.0.0.1:1080;SOCKS 127.0.0.1:1080;SOCKS5 127.0.0.1:48102;SOCKS5 127.0.0.1:65500;SOCKS5 127.0.0.1:7070;PROXY 127.0.0.1:8087;SOCKS5 192.168.2.1:1080;PROXY 127.0.0.1:8080;SOCKS 127.0.0.1:1081;" + direct; };
//var wall_v6_proxy = function(){ return direct+";PROXY [fe80::c0a8:201]:8118;PROXY [0::7f00:1]:8118;SOCKS5 [0::7f00:1]:1080;SOCKS [0::7f00:1]:1080;SOCKS5 [0::7f00:1]:48102;SOCKS5 [0::7f00:1]:65500;SOCKS5 [0::7f00:1]:7070;PROXY [0::7f00:1]:8087;SOCKS5 [fe80::c0a8:201]:1080;PROXY [0::7f00:1]:8080;SOCKS [0::7f00:1]:1081;" + direct; };

//-----------------------以下是CN.IP地址段-------------------------------

var cnIpRange = [
{},{0x10001:1,0x10002:1,0x10003:1,0x10008:4,0x1000c:4,0x10020:16,0x10030:16,0x10100:1,0x10102:1,0xdfffec:4,0xdffffc:2}
];

var cnIp16Range = {
0x400:1,0x404:1,0x408:1,0x410:1,0x428:1,0x3800:1,0x3804:1,0x399a:1,0x3b00:1,0x3b01:1,0x6c8b:1,0x373de:1,0x3741c:1,0x3741d:1,0x3742f:1,0x37435:1,0x37617:1,0x3771c:1,0x3771f:1,0x37a8c:1,0x37be6:1,0x37c6e:1,0x37f7e:1,0x37f7f:1,0x37fff:1
};

var subnetIpRangeList = [
167772160,184549376,    //10.0.0.0/8
2886729728,2887778304,    //172.16.0.0/12
3232235520,3232301056,    //192.168.0.0/16
2130706432,2130706688    //127.0.0.0/24
];

var list = ["""%(proxy)
    intLines = 0
    for ip,mask,_ in results:
        if intLines > 0:
            strLines = strLines + ','
        intLines = intLines + 1
        strLines = strLines + """
    [%d, %d]"""%(ip, mask)
    strLines = strLines + """
];

var fakeIps = {
    '74.125.127.102'  : 1,
    '74.125.155.102'  : 1,
    '74.125.39.102'   : 1,
    '74.125.39.113'   : 1,
    '209.85.229.138'  : 1,
    '128.121.126.139' : 1,
    '159.106.121.75'  : 1,
    '169.132.13.103'  : 1,
    '192.67.198.6'    : 1,
    '202.106.1.2'     : 1,
    '202.181.7.85'    : 1,
    '203.161.230.171' : 1,
    '203.98.7.65'     : 1,
    '207.12.88.98'    : 1,
    '208.56.31.43'    : 1,
    '209.145.54.50'   : 1,
    '209.220.30.174'  : 1,
    '209.36.73.33'    : 1,
    '211.94.66.147'   : 1,
    '213.169.251.35'  : 1,
    '216.221.188.182' : 1,
    '216.234.179.13'  : 1,
    '243.185.187.39'  : 1,
    '37.61.54.158'    : 1,
    '4.36.66.178'     : 1,
    '46.82.174.68'    : 1,
    '59.24.3.173'     : 1,
    '64.33.88.161'    : 1,
    '64.33.99.47'     : 1,
    '64.66.163.251'   : 1,
    '65.104.202.252'  : 1,
    '65.160.219.113'  : 1,
    '66.45.252.237'   : 1,
    '72.14.205.104'   : 1,
    '72.14.205.99'    : 1,
    '78.16.49.15'     : 1,
    '8.7.198.45'      : 1,
    '93.46.8.89'      : 1
};

var safePorts = {
    5223  : 1,
    3478  : 1
};

//----------------以下是需要屏蔽的host主机网址-----------------------

var blackhole_host = {
    'www.36595501.com': 1,
    '118.26.200.246': 1,
    '122.227.254.195': 1
};

var dangerDomains = {
    'www.36595501.com' : 1,
    'wap.jrnapkin.cn' : 1
};


//----------------以下是确认需要翻墙的host主机网址----------------------


var domains = """+proxy_content+""";

var autoproxy_host = {
    "0rz.tw": 1,
    "0to255.com": 1,
    "1-apple.com.tw": 1,
    "10musume.com": 1
};

var gfwed_list = [
    "akamai.net",
    "akamaihd.net",
    "amazon.com",
    "appspot.com",
    "archive.org",
    "bitly.com",
    "blogger.com",
    "blogspot.com",
    "cl.ly",
    "facebook.com",
    "fbcdn.net",
    "feedburner.com",
    "feedsportal.com",
    "gmail.com",
    "goo.gl",
    "google.com",
    "j.mp",
    "mediafire.com",
    "openvpn.net",
    "osfoora.com",
    "posterous.com",
    "rapidshare.com",
    "t.co",
    "twimg.com",
    "twitpic.com",
    "twitter.com",
    "vimeo.com",
    "wordpress.com",
    "yfrog.com",
    "youtube.com",
    "ytimg.com"
];


//----------------以下是需要直连的host主机网址-----------------------

var whitehole_host = {
    '*baidu.com': 1,
    '118.26.200.246': 1,
    '122.227.254.195': 1
};

var safeDomains = {
    '10010.com' : 1,
    '115.com' : 1,
    '123u.com' : 1,
    '126.com' : 1,
    '126.net' : 1,
    '163.com' : 1,
    '17173.com' : 1,
    '178.com' : 1,
    '17cdn.com' : 1,
    '21cn.com' : 1,
    '2288.org' : 1,
    '3322.org' : 1,
    '360buy.com' : 1,
    '360buyimg.com' : 1,
    '360doc.com' : 1,
    '360safe.com' : 1,
    '36kr.com' : 1,
    '400gb.com' : 1,
    '4399.com' : 1,
    '51.la' : 1,
    '51buy.com' : 1,
    '51cto.com' : 1,
    '51job.com' : 1,
    '51jobcdn.com' : 1,
    '5d6d.com' : 1,
    '5d6d.net' : 1,
    '61.com' : 1,
    '6600.org' : 1,
    '6rooms.com' : 1,
    '7766.org' : 1,
    '7k7k.com' : 1,
    '8800.org' : 1,
    '8866.org' : 1,
    '90g.org' : 1,
    '91.com' : 1,
    '9966.org' : 1,
    'acfun.tv' : 1,
    'aicdn.com' : 1,
    'ali213.net' : 1,
    'alibaba.com' : 1,
    'alicdn.com' : 1,
    'aliexpress.com' : 1,
    'aliimg.com' : 1,
    'alikunlun.com' : 1,
    'alimama.com' : 1,
    'alipay.com' : 1,
    'alipayobjects.com' : 1,
    'alisoft.com' : 1,
    'aliyun.com' : 1,
    'aliyuncdn.com' : 1,
    'aliyuncs.com' : 1,
    'anzhi.com' : 1,
    'appinn.com' : 1,
    'appdownload.itunes.apple.com' : 1,
    'apple.com' : 1,
    'appsina.com' : 1,
    'archlinuxcn.org' : 1,
    'atpanel.com' : 1,
    'baidu.com' : 1,
    'baidupcs.com' : 1,
    'baidustatic.com' : 1,
    'baifendian.com' : 1,
    'baihe.com' : 1,
    'baixing.com' : 1,
    'bdimg.com' : 1,
    'bdstatic.com' : 1,
    'bilibili.tv' : 1,
    'blogbus.com' : 1,
    'blueidea.com' : 1,
    'ccb.com' : 1,
    'cctv.com' : 1,
    'cctvpic.com' : 1,
    'cdn20.com' : 1,
    'china.com' : 1,
    'chinabyte.com' : 1,
    'chinacache.com' : 1,
    'chinacache.net' : 1,
    'chinacaipu.com' : 1,
    'chinagba.com' : 1,
    'chinahr.com' : 1,
    'chinajoy.net' : 1,
    'chinamobile.com' : 1,
    'chinanetcenter.com' : 1,
    'chinanews.com' : 1,
    'chinapnr.com' : 1,
    'chinaren.com' : 1,
    'chinaspeeds.net' : 1,
    'chinaunix.net' : 1,
    'chinaz.com' : 1,
    'chint.com' : 1,
    'chiphell.com' : 1,
    'chuangxin.com' : 1,
    'ci123.com' : 1,
    'ciku5.com' : 1,
    'citysbs.com' : 1,
    'class.coursera.org' : 1,
    'cloudcdn.net' : 1,
    'cmbchina.com' : 1,
    'cmfu.com' : 1,
    'cmread.com' : 1,
    'cmwb.com' : 1,
    'cn.archive.ubuntu.com' : 1,
    'cn.bing.com' : 1,
    'cn.coremetrics.com' : 1,
    'cn.debian.org' : 1,
    'cn.msn.com' : 1,
    'cn' : 1,
    'cnak2.englishtown.com' : 1,
    'cnbeta.com' : 1,
    'cnbetacdn.com' : 1,
    'cnblogs.com' : 1,
    'cnepub.com' : 1,
    'cnzz.com' : 1,
    'comsenz.com' : 1,
    'csdn.net' : 1,
    'ct10000.com' : 1,
    'ctdisk.com' : 1,
    'dangdang.com' : 1,
    'dbank.com' : 1,
    'dedecms.com' : 1,
    'diandian.com' : 1,
    'dianping.com' : 1,
    'discuz.com' : 1,
    'discuz.net' : 1,
    'dl.google.com' : 1,
    'docin.com' : 1,
    'donews.com' : 1,
    'dospy.com' : 1,
    'douban.com' : 1,
    'douban.fm' : 1,
    'duapp.com' : 1,
    'duba.net' : 1,
    'duomi.com' : 1,
    'duote.com' : 1,
    'duowan.com' : 1,
    'egou.com' : 1,
    'et8.org' : 1,
    'etao.com' : 1,
    'f3322.org' : 1,
    'fantong.com' : 1,
    'fenzhi.com' : 1,
    'fhldns.com' : 1,
    'ganji.com' : 1,
    'gaopeng.com' : 1,
    'geekpark.net' : 1,
    'gfan.com' : 1,
    'gtimg.com' : 1,
    'hacdn.net' : 1,
    'hadns.net' : 1,
    'hao123.com' : 1,
    'hao123img.com' : 1,
    'hc360.com' : 1,
    'hdslb.com' : 1,
    'hexun.com' : 1,
    'hiapk.com' : 1,
    'hichina.com' : 1,
    'hoopchina.com' : 1,
    'huanqiu.com' : 1,
    'hudong.com' : 1,
    'huochepiao.com' : 1,
    'hupu.com' : 1,
    'iask.com' : 1,
    'iciba.com' : 1,
    'idqqimg.com' : 1,
    'ifanr.com' : 1,
    'ifeng.com' : 1,
    'ifengimg.com' : 1,
    'ijinshan.com' : 1,
    'iqiyi.com' : 1,
    'it168.com' : 1,
    'itcpn.net' : 1,
    'iteye.com' : 1,
    'itouzi.com' : 1,
    'jandan.net' : 1,
    'jd.com' : 1,
    'jiashule.com' : 1,
    'jiasule.com' : 1,
    'jiathis.com' : 1,
    'jiayuan.com' : 1,
    'jiepang.com' : 1,
    'jing.fm' : 1,
    'jobbole.com' : 1,
    'jstv.com' : 1,
    'jumei.com' : 1,
    'kaixin001.com' : 1,
    'kandian.com' : 1,
    'kandian.net' : 1,
    'kanimg.com' : 1,
    'kankanews.com' : 1,
    'kdnet.net' : 1,
    'koudai8.com' : 1,
    'ku6.com' : 1,
    'ku6cdn.com' : 1,
    'ku6img.com' : 1,
    'kuaidi100.com' : 1,
    'kugou.com' : 1,
    'lashou.com' : 1,
    'letao.com' : 1,
    'letv.com' : 1,
    'lietou.com' : 1,
    'linezing.com' : 1,
    'loli.mg' : 1,
    'loli.vg' : 1,
    'lvping.com' : 1,
    'lxdns.com' : 1,
    'mangocity.com' : 1,
    'mapbar.com' : 1,
    'mcbbs.net' : 1,
    'mediav.com' : 1,
    'meilishuo.com' : 1,
    'meituan.com' : 1,
    'meituan.net' : 1,
    'meizu.com' : 1,
    'microsoft.com' : 1,
    'miui.com' : 1,
    'moe123.com' : 1,
    'moegirl.org' : 1,
    'mop.com' : 1,
    'mtime.com' : 1,
    'my-card.in' : 1,
    'mydrivers.com' : 1,
    'mzstatic.com' : 1,
    'netease.com' : 1,
    'newsmth.net' : 1,
    'ngacn.cc' : 1,
    'nuomi.com' : 1,
    'okbuy.com' : 1,
    'optaim.com' : 1,
    'oschina.net' : 1,
    'paipai.com' : 1,
    'pcbeta.com' : 1,
    'pchome.net' : 1,
    'pcpop.com' : 1,
    'pengyou.com' : 1,
    'phoenixlzx.com' : 1,
    'phpwind.net' : 1,
    'pingan.com' : 1,
    'pool.ntp.org' : 1,
    'pplive.com' : 1,
    'pps.tv' : 1,
    'ppstream.com' : 1,
    'pptv.com' : 1,
    'pubyun.com' : 1,
    'qhimg.com' : 1,
    'qianlong.com' : 1,
    'qidian.com' : 1,
    'qingdaonews.com' : 1,
    'qiniu.com' : 1,
    'qiniudn.com' : 1,
    'qiushibaike.com' : 1,
    'qiyi.com' : 1,
    'qiyipic.com' : 1,
    'qq.com' : 1,
    'qqmail.com' : 1,
    'qstatic.com' : 1,
    'qunar.com' : 1,
    'qunarzz.com' : 1,
    'qvbuy.com' : 1,
    'renren.com' : 1,
    'renrendai.com' : 1,
    'rrfmn.com' : 1,
    'rrimg.com' : 1,
    'sanguosha.com' : 1,
    'sdo.com' : 1,
    'sina.com' : 1,
    'sinaapp.com' : 1,
    'sinaedge.com' : 1,
    'sinaimg.com' : 1,
    'sinajs.com' : 1,
    'skycn.com' : 1,
    'smzdm.com' : 1,
    'sogou.com' : 1,
    'sohu.com' : 1,
    'soku.com' : 1,
    'solidot.org' : 1,
    'soso.com' : 1,
    'soufun.com' : 1,
    'soufunimg.com' : 1,
    'staticfile.org' : 1,
    'staticsdo.com' : 1,
    'steamcn.com' : 1,
    'suning.com' : 1,
    'szzfgjj.com' : 1,
    'tanx.com' : 1,
    'taobao.com' : 1,
    'taobaocdn.com' : 1,
    'tbcache.com' : 1,
    'tdimg.com' : 1,
    'tencent.com' : 1,
    'tenpay.com' : 1,
    'tgbus.com' : 1,
    'thawte.com' : 1,
    'tiancity.com' : 1,
    'tianyaui.com' : 1,
    'tiexue.net' : 1,
    'tmall.com' : 1,
    'tmcdn.net' : 1,
    'tom.com' : 1,
    'tomonline-inc.com' : 1,
    'tuan800.com' : 1,
    'tuan800.net' : 1,
    'tuanimg.com' : 1,
    'tudou.com' : 1,
    'tudouui.com' : 1,
    'tuniu.com' : 1,
    'u148.net' : 1,
    'u17.com' : 1,
    'ubuntu.com' : 1,
    'ucjoy.com' : 1,
    'uni-marketers.com' : 1,
    'unionpay.com' : 1,
    'unionpaysecure.com' : 1,
    'upaiyun.com' : 1,
    'upyun.com' : 1,
    'uusee.com' : 1,
    'uuu9.com' : 1,
    'vaikan.com' : 1,
    'vancl.com' : 1,
    'vcimg.com' : 1,
    'verycd.com' : 1,
    'wandoujia.com' : 1,
    'wdjimg.com' : 1,
    'weibo.com' : 1,
    'weiphone.com' : 1,
    'weiyun.com' : 1,
    'west263.com' : 1,
    'wrating.com' : 1,
    'wscdns.com' : 1,
    'wumii.com' : 1,
    'xdcdn.net' : 1,
    'xiachufang.com' : 1,
    'xiami.com' : 1,
    'xiami.net' : 1,
    'xiaomi.com' : 1,
    'xiaonei.com' : 1,
    'xiazaiba.com' : 1,
    'xici.net' : 1,
    'xilu.com' : 1,
    'xinhuanet.com' : 1,
    'xinnet.com' : 1,
    'xlpan.com' : 1,
    'xn--fiqs8s' : 1,
    'xnpic.com' : 1,
    'xungou.com' : 1,
    'xunlei.com' : 1,
    'ydstatic.com' : 1,
    'yesky.com' : 1,
    'yeyou.com' : 1,
    'yihaodian.com' : 1,
    'yihaodianimg.com' : 1,
    'yingjiesheng.com' : 1,
    'yintai.com' : 1,
    'yinyuetai.com' : 1,
    'yiqifa.com' : 1,
    'yixun.com' : 1,
    'ykimg.com' : 1,
    'ynet.com' : 1,
    'youdao.com' : 1,
    'yougou.com' : 1,
    'youku.com' : 1,
    'yupoo.com' : 1,
    'yy.com' : 1,
    'zbjimg.com' : 1,
    'zhaopin.com' : 1,
    'zhi.hu' : 1,
    'zhihu.com' : 1,
    'zhimg.com' : 1,
    'zhubajie.com' : 1,
    'zongheng.com' : 1
};


//----------------以下是对象合并、选择和处理-----------------------

//var o1={hello:1},o2={world:2};
//extend(o1,o2);
extend(autoproxy_host,domains);
extend(dangerDomains,blackhole_host);
extend(safeDomains,whitehole_host);
var autoproxy_host = domains   //以domains为准
//var domains = autoproxy_host   //以autoproxy_host为准
var dangerDomains = blackhole_host  //以blackhole_host为准
//var blackhole_host = dangerDomains  //以dangerDomains为准
var whitehole_host = safeDomains  //以safeDomains为准
//var safeDomains = whitehole_host  //以whitehole_host为准
var gfwed = {};
for (var i = 0; i < gfwed_list.length; i += 1) {
    gfwed[gfwed_list[i]] = true;
}
extend(autoproxy_host,gfwed);
extend(domains,autoproxy_host);


//-----------------------------------------------------------------

function host2domain(host) {
    var dotpos = host.lastIndexOf(".");
    if (dotpos === -1)
        return host;
    // Find the second last dot
    dotpos = host.lastIndexOf(".", dotpos - 1);
    if (dotpos === -1)
        return host;
    return host.substring(dotpos + 1);
};
function FindProxyForURLByAdblock(url, host) {
    // untrusted ablock plus list, disable whitelist until chinalist come back.
    if (blackhole_host.hasOwnProperty(host)) {
        return blackhole;
    }
    return direct;
}
function FindProxyForURLByAutoProxy(url, host) {
    var lastPos;
    var host_tmp=host;
    do {
        if (autoproxy_host.hasOwnProperty(host_tmp)) {
            return wall_proxy();
        }
        lastPos = host_tmp.indexOf('.') + 1;
        host_tmp = host_tmp.slice(lastPos);
    } while (lastPos >= 1);
    var strIp = dnsResolve(host);
    if ( !strIp ) {
        return wall_proxy();
    } else if (fakeIps[strIp]) {
        return wall_proxy();
    } else { return getProxyFromIPEx(strIp); }
    return direct;
}
function check_ipv4(host) {
    var re_ipv4 = /^\d+\.\d+\.\d+\.\d+$/g;
    if (re_ipv4.test(host)) {
        return true;
    }
}
function check_ipv6(host) {
    var re_ipv6 = /^\[?([a-fA-F0-9]{0,4}\:){1,7}[a-fA-F0-9]{0,4}\]?$/g;
    if (re_ipv6.test(host)) {
        return true;
    }
}
function check_ipv6_dns(dnsstr) {
    var re_ipv6 = /([a-fA-F0-9]{0,4}\:){1,7}[a-fA-F0-9]{0,4}(%[0-9]+)?/g;
    if (re_ipv6.test(dnsstr)) {
        return true;
    }
}
function convertAddress(ipchars) {
    var bytes = ipchars.split('.');
    var result = (bytes[0] << 24) |
    (bytes[1] << 16) |
    (bytes[2] << 8) |
    (bytes[3]);
    return result >>> 0;
};
function isInSingleRange(ipRange, intIp) {
    if ( hasOwnProperty.call(cnIp16Range, intIp >>> 6) ) {
        for ( var range = 1; range < 64; range*=4 ) {
            var master = intIp & ~(range-1);
            if ( hasOwnProperty.call(ipRange, master) )
                return intIp - master < ipRange[master];
        }
    } else {
        for ( var range = 64; range <= 1024; range*=4 ) {
            var master = intIp & ~(range-1);
            if ( hasOwnProperty.call(ipRange, master) )
                return intIp - master < ipRange[master];
        }
    }
}
function isInSubnetRange(ipRange, intIp) {
    for ( var i = 0; i < 8; i += 2 ) {
        if ( ipRange[i] <= intIp && intIp < ipRange[i+1] )
            return true;
    }
}
function convertAddressEx(ipchars) {
    var bytes = ipchars.split('.');
    var result = ((bytes[0] & 0xff) << 24) |
                 ((bytes[1] & 0xff) << 16) |
                 ((bytes[2] & 0xff) <<  8) |
                  (bytes[3] & 0xff);
    return result >>> 0;
}
function hostindomainsex(domains, host) {
    var suffix;
    var pos = host.lastIndexOf('.');
    pos = host.lastIndexOf('.', pos - 1);
    while(1) {
    if (pos == -1) {
        if (hasOwnProperty.call(domains, host)) {
            return true;
        } else {
            return false;
        }
    }
    suffix = host.substring(pos + 1);
    //return domains['*.youtube.com'];
    if (hasOwnProperty.call(domains, suffix)) {
        return true;
    }
        pos = host.lastIndexOf('.', pos - 1);
    }
}
function hostindomains(domains, host) {
    for(var i in domains){
        if (shExpMatch(host,i) ||
               dnsDomainIs(host,i) ||
               host == i) {
            //return i;
            return true;
        }
    }
    return false;
}
function testDomain(target, domains, cnRootIncluded) {
    var idxA = target.lastIndexOf('.');
    var idxB = target.lastIndexOf('.', idxA - 1);
    var hasOwnProperty = Object.hasOwnProperty;
    var suffix = cnRootIncluded ? target.substring(idxA + 1) : '';
    if (suffix === 'cn') {
        return true;
    }
    while (true) {
        if (idxB === -1) {
            if (hasOwnProperty.call(domains, target)) {
                return true;
            } else {
                return false;
            }
        }
        suffix = target.substring(idxB + 1);
        if (hasOwnProperty.call(domains, suffix)) {
            return true;
        }
        idxB = target.lastIndexOf('.', idxB - 1);
    }
}
function match(ip, list) {
    if (list.length == 0) {
      return false;
    }
    var left = 0, right = list.length;
    do {
        var mid = Math.floor((left + right) / 2),
            ip_f  = (ip & list[mid][1]) >>> 0,
            m   = (list[mid][0] & list[mid][1]) >>> 0;
        if (ip_f == m) {
            return true;
        } else if (ip_f > m) {
            left  = mid + 1;
        } else {
            right = mid;
        }
    } while (left + 1 <= right);
    return false;
}
function getProxyFromIP(strIp) {
    if ( !check_ipv4(strIp) === true ) {
        return ipv6_proxy();
    }
    //if ( check_ipv6(strIp) === true ) {
    //    return ipv6_proxy();
    //}
    var intIp = convertAddress(strIp);
    if (isInNet(strIp, "10.0.0.0", "255.0.0.0") || isInNet(strIp, "172.16.0.0",  "255.240.0.0") || isInNet(strIp, "192.168.0.0", "255.255.0.0") || isInNet(strIp, "127.0.0.0", "255.255.255.0")) {
        return direct;
    }
    var index = (intIp >>> 24) & 0xff;
    if ( isInSingleRange(cnIpRange[index], intIp >>> 8) ) {
        return nowall_proxy();
    }
    return wall_proxy();
}
function getProxyFromIPEx(strIp) {
    var intIp = convertAddressEx(strIp);
    //return intIp;
    if ( isInSubnetRange(subnetIpRangeList, intIp) ) {
        return direct;
    }
    //var index = ((intIp & 0xff000000) >>> 0 ) % 255;
    //return list[index];
    //if (match(intIp, list[index])) {
    if (match(intIp, list)) {
        return direct;
    }
    return wall_proxy();
}



//-----------------------------------------------------------------


function FindProxyForURL_BAK_1(url, host) {
    url = url.toLowerCase();
    host = host.toLowerCase();
    if (hostindomains(dangerDomains, host)) {
        return block();
    }
    if (hostindomains(domains, host)) {
        return wall_proxy();
    }
    if (shExpMatch(host, "*.cn")) {
        return nowall_proxy();
    }
    if ((isPlainHostName(host) === true ) || (host === '127.0.0.1') || (host === 'localhost')) {
        return direct;
    }
    if ( check_ipv4(host) === true ) {
        return getProxyFromIP(host);
    }
    if ( check_ipv6(host) === true ) {
        return ipv6_proxy();
    }
    var strIp = dnsResolve(host);
    if ( !strIp ) {
        return wall_proxy();
    }
    return getProxyFromIP(strIp);
}
function FindProxyForURLEx_BAK_1(url, host) {
    url = url.toLowerCase();
    host = host.toLowerCase();
    if (testDomain(host, dangerDomains)) {
        return block();
    }
    if (testDomain(host, domains, true)) {
        return wall_proxy();
    }
    if (shExpMatch(host, "*.cn")) {
        return nowall_proxy();
    }
    if ((isPlainHostName(host) === true ) || (host === '127.0.0.1') || (host === 'localhost')) {
        return direct;
    }
    if ( check_ipv4(host) === true ) {
        return getProxyFromIP(host);
    }
    if ( check_ipv6(host) === true ) {
        return ipv6_proxy();
    }
    var strIp = dnsResolveEx(host);
    if ( !strIp ) {
        return wall_proxy();
    }
    if ( check_ipv6_dns(strIp) === true ) {
        return ipv6_proxy();
    }
    var dnsIps = strIp.split(";");
    if (check_ipv4(dnsIps[0]) === true) {
        return getProxyFromIPEx(dnsIps[0]);
    } else if (check_ipv6_dns(dnsIps[0]) === true) {
        return ipv6_proxy();
    }
    return wall_proxy();
}

//-----------------------------------------------------------------


function FindProxyForURL_ORG(url, host) {
    var autoproxy = 'PROXY 127.0.0.1:8087';
    var blackhole = 'PROXY 127.0.0.1:8086';
    var defaultproxy = 'DIRECT';
    if (isPlainHostName(host) ||
        host.indexOf('127.') == 0 ||
        host.indexOf('192.168.') == 0 ||
        host.indexOf('10.') == 0 ||
        shExpMatch(host, 'localhost.*')) {
        return 'DIRECT';
    } else if (FindProxyForURLByAdblock(url, host) != defaultproxy ||
               host == 'p.tanx.com' ||
               host == 'a.alimama.cn' ||
               host == 'pagead2.googlesyndication.com' ||
               dnsDomainIs(host, '.google-analytics.com') ||
               dnsDomainIs(host, '.2mdn.net') ||
               dnsDomainIs(host, '.doubleclick.net')) {
        return blackhole;
    } else if (shExpMatch(host, '*.google*.*') ||
               dnsDomainIs(host, '.ggpht.com') ||
               dnsDomainIs(host, '.wikipedia.org') ||
               host == 'cdnjs.cloudflare.com' ||
               host == 'wp.me' ||
               host == 'po.st' ||
               host == 'goo.gl') {
        return autoproxy;
    } else {
        return FindProxyForURLByAutoProxy(url, host);
    }
}




//-----------------------------------------------------------------


function FindProxyForURL(url, host) {
    //return gfwed[host2domain(host)] ? http_proxy : direct;
    //return hostindomains(safeDomains, host);
    //return getProxyFromIPEx("180.97.33.107");
    //return getProxyFromIPEx("159.106.121.75");
    //return getProxyFromIPEx("114.114.114.114");
    //return getProxyFromIPEx("8.8.8.8");
    //return o1.world;
    //return o2.hello;
    url = url.toLowerCase();
    host = host.toLowerCase();
    if (isPlainHostName(host) ||
        host.indexOf('127.') == 0 ||
        host.indexOf('192.168.') == 0 ||
        host.indexOf('10.') == 0 ||
        shExpMatch(host, 'localhost.*')) {
        return direct;
    } else if (hostindomains(blackhole_host, host) ||
               //host == 'p.tanx.com' ||
               //host == 'a.alimama.cn' ||
               //host == 'pagead2.googlesyndication.com' ||
               //dnsDomainIs(host, '.google-analytics.com') ||
               //dnsDomainIs(host, '.doubleclick.net') ||
               //dnsDomainIs(host, '.2mdn.net') ||
               FindProxyForURLByAdblock(url, host) != defaultproxy) {
        return blackhole;
    } else if (shExpMatch(host, '*.google*.*') ||
               dnsDomainIs(host, '*.youtube.com') ||
               dnsDomainIs(host, '*.twitter.com') ||
               //dnsDomainIs(host, '.ggpht.com') ||
               //dnsDomainIs(host, '.wikipedia.org') ||
               //host == 'goo.gl') ||
               //host == 'cdnjs.cloudflare.com' ||
               //host == 'wp.me' ||
               //host == 'po.st' ||
               dnsDomainIs(host, '*.facebook.com')) {
        return autoproxy;
    } else if (shExpMatch(host, "*.cn") ||
               hostindomains(whitehole_host, host)) {
        return nowall_proxy();
    } else {
        return FindProxyForURLByAutoProxy(url, host);
    }
}
function FindProxyForURLEX(url, host) {
    //url = url.toLowerCase();
    //host = host.toLowerCase();
    if (isPlainHostName(host) ||
        host.indexOf('127.') == 0 ||
        host.indexOf('192.168.') == 0 ||
        host.indexOf('10.') == 0 ||
        shExpMatch(host, 'localhost.*')) {
        return direct;
    } else if (hostindomains(blackhole_host, host) ||
               //host == 'p.tanx.com' ||
               //host == 'a.alimama.cn' ||
               //host == 'pagead2.googlesyndication.com' ||
               //dnsDomainIs(host, '.google-analytics.com') ||
               //dnsDomainIs(host, '.doubleclick.net') ||
               //dnsDomainIs(host, '.2mdn.net') ||
               FindProxyForURLByAdblock(url, host) != defaultproxy) {
        return blackhole;
    } else if (shExpMatch(host, '*.google*.*') ||
               dnsDomainIs(host, '*.youtube.com') ||
               dnsDomainIs(host, '*.twitter.com') ||
               //dnsDomainIs(host, '.ggpht.com') ||
               //dnsDomainIs(host, '.wikipedia.org') ||
               //host == 'goo.gl') ||
               //host == 'cdnjs.cloudflare.com' ||
               //host == 'wp.me' ||
               //host == 'po.st' ||
               dnsDomainIs(host, '*.facebook.com')) {
        return autoproxy;
    } else if (shExpMatch(host, "*.cn") ||
               hostindomains(whitehole_host, host)) {
        return nowall_proxy();
    } else {
        return FindProxyForURLByAutoProxy(url, host);
    }
}


    """
    rfile.write(strLines)
    rfile.close()
    print ("Rules: %d items.\n"
           "Usage: Use the newly created %s as your web browser's automatic "
           "PAC(Proxy auto-config) file."%(intLines, pacfile))


def fetch_ip_data_leask():
    global n,results,test,d3,day
    if not os.path.exists('test.txt'):
        d3=8
        day=0
    if d3<day:
        test=1
        if n==0:print 'no need to update.'
        n=1
    if n==1:return results
    n=1
    #fetch data from apnic
    print "Fetching data from apnic.net, it might take a few minutes, please wait..."
    if not test==1 or not os.path.exists('test.txt'):
        if(sysstr =="Windows"):
            if os.path.exists('wget.exe'):os.system("wget --no-check-certificate -c http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O test.txt")
            else:
                url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
                data=urllib2.urlopen(url).read()
                open('test.txt','w').write(data)
        elif(sysstr =="Linux"):
            os.system("wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O test.txt")
        else:
            url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
            data=urllib2.urlopen(url).read()
            open('test.txt','w').write(data)
    data=open('test.txt').read()
    #print data

    cnregex=re.compile(r'apnic\|cn\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',re.IGNORECASE)
    cndata=cnregex.findall(data)

    results=[]
    prev_net=''

    for item in cndata:
        unit_items=item.split('|')
        starting_ip=unit_items[3]
        num_ip=int(unit_items[4])

        imask=0xffffffff^(num_ip-1)
        #convert to string
        imask=hex(imask)[2:]
        mask=[0]*4
        mask[0]=imask[0:2]
        mask[1]=imask[2:4]
        mask[2]='0' #imask[4:6]
        mask[3]='0' #imask[6:8]

        #convert str to int
        mask=[ int(i,16 ) for i in mask]
        mask="%d.%d.%d.%d"%tuple(mask)

        #mask in *nix format
        mask2=32-int(math.log(num_ip,2))

        ip=starting_ip.split('.')
        ip[2] = '0'
        ip[3] = '0'
        starting_ip = '.'.join(ip)
        if starting_ip != prev_net:
            results.append((ip2long(starting_ip), ip2long(mask), mask2))
            prev_net = starting_ip

    return results











def generate_ovpn(metric):
    global results,d3,day,ng
    #print d3,day
    fetch_ip_data()
    if d3<day:return
    ct=''
    for ip,mask,_ in results:
        if ng=='':route_item="route %s %s net_gateway %d\n"%(ip,mask,metric)
        else:route_item="route %s %s %s %d\n"%(ip,mask,ng.replace('\'',''),metric)
        ct+=route_item
    open('routes.txt','w').write(ct)

    #print "Usage: Append the content of the newly created routes.txt to your openvpn config file," \
    #      " and also add 'max-routes %d', which takes a line, to the head of the file." % (len(results)+20)
    return

def generate_ovpn_plus(metric):
    global results,d3,day,ng
    #print d3,day
    fetch_ip_data()
    if d3<day:return
    ct=''
    for ip,mask,_ in results:
        if ng=='':route_item="route %s %s net_gateway %d\n"%(ip,mask,metric)
        else:route_item="route %s %s %s %d\n"%(ip,mask,ng.replace('\'',''),metric)
        ct+=route_item
    open('routes.txt','w').write(ct)
    items = os.listdir(".")
    for names in items:
        if names.endswith(".ovpn"):
            if not 'max-routes' in open(names).read():
                open(names, 'a').write(ct)
                with open(names) as f:
                    lines = f.readlines()
                    lines.insert(0, 'max-routes %d\n'%(len(results)+60))
                    lines.insert(0, 'route-delay 2\n')
                    lines.insert(0, 'route-method exe\n')
                    open(names, 'w').writelines(lines)

    #print "Usage: Append the content of the newly created routes.txt to your openvpn config file," \
    #      " and also add 'max-routes %d', which takes a line, to the head of the file." % (len(results)+20)
    return

def generate_linux(metric):
    global d3,day,results
    fetch_ip_data()
    if d3<day:return

    upscript_header=textwrap.dedent("""\
#!/bin/sh
#alias nestat='/bin/netstat'
#alias grep='/bin/grep'
#alias awk='/bin/busybox awk'
#alias route='/sbin/route'

OLDGW=`netstat -rn | grep 255\.255\.255\.255 | grep ppp0 | awk '{print $1}'`
#OLDGW='192.168.2.1'
NEWGW=`netstat -rn | grep ^0\.0\.0\.0 | awk '{print $2}'`
#OLDGW=`netstat -rn | grep ^0\.0\.0\.0 | awk '{print $2}'`

#echo $OLDGW
#exit 1

    """)

    downscript_header=textwrap.dedent("""\
#!/bin/sh
#alias nestat='/bin/netstat'
#alias grep='/bin/grep'
#alias awk='/bin/busybox awk'
#alias route='/sbin/route'

    """)

    upfile=open('vpnup_linux.sh','w')
    #downfile=open('vpndown_linux.sh','w')

    upfile.write(upscript_header)
    upfile.write('\n')
    #downfile.write(downscript_header)
    #downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('route add -net %s netmask %s gw $OLDGW\n'%(ip,mask))
        #downfile.write('route del -net %s netmask %s\n'%(ip,mask))

    upfile.close()
    #downfile.close()

    #print "Old school way to call up/down script from openvpn client. " \
    #      "use the regular openvpn 2.1 method to add routes if it's possible"
    return

def generate_linux_bak(metric):
    global results,d3,day
    if d3<day:
        print 'no need to update.'
        return
    fetch_ip_data()
    upscript_header=textwrap.dedent("""\
#!/bin/bash
export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

OLDGW=`ip route show | grep '^default' | sed -e 's/default via \\([^ ]*\\).*/\\1/'`
#OLDGW='192.168.2.1'

if [ $OLDGW == '' ]; then
    exit 0
fi

if [ ! -e /tmp/vpn_oldgw ]; then
    echo $OLDGW > /tmp/vpn_oldgw
fi

    """)

    downscript_header=textwrap.dedent("""\
#!/bin/bash
export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

OLDGW=`cat /tmp/vpn_oldgw`
#OLDGW='192.168.2.1'

    """)

    upfile=open('ip-pre-up_linux','w')
    #downfile=open('ip-down_linux','w')

    upfile.write(upscript_header)
    upfile.write('\n')
    #downfile.write(downscript_header)
    #downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('route add -net %s netmask %s gw $OLDGW\n'%(ip,mask))
        #downfile.write('route del -net %s netmask %s\n'%(ip,mask))

    #downfile.write('rm /tmp/vpn_oldgw\n')

    #print "For pptp only, please copy the file ip-pre-up to the folder/etc/ppp," \
    #      "and copy the file ip-down to the folder /etc/ppp/ip-down.d."
    return

def generate_mac(metric):
    global d3,day,results
    fetch_ip_data()
    if d3<day:return

    upscript_header=textwrap.dedent("""\
#!/bin/sh
export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

OLDGW=`netstat -nr | grep '^default' | grep -v 'ppp' | sed 's/default *\\([0-9\.]*\\) .*/\\1/' | awk '{if($1){print $1}}'`
#OLDGW='192.168.2.1'

if [ ! -e /tmp/pptp_oldgw ]; then
    echo "${OLDGW}" > /tmp/pptp_oldgw
fi

dscacheutil -flushcache

route add 10.0.0.0/8 "${OLDGW}"
route add 172.16.0.0/12 "${OLDGW}"
route add 192.168.0.0/16 "${OLDGW}"
    """)

    downscript_header=textwrap.dedent("""\
#!/bin/sh
export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

if [ ! -e /tmp/pptp_oldgw ]; then
        exit 0
fi

ODLGW=`cat /tmp/pptp_oldgw`
#OLDGW='192.168.2.1'

route delete 10.0.0.0/8 "${OLDGW}"
route delete 172.16.0.0/12 "${OLDGW}"
route delete 192.168.0.0/16 "${OLDGW}"
    """)

    upfile=open('ip-up_mac','w')
    #downfile=open('ip-down_mac','w')


    upfile.write(upscript_header)
    upfile.write('\n')
    #downfile.write(downscript_header)
    #downfile.write('\n')

    for ip,_,mask in results:
        upfile.write('route add %s/%s "${OLDGW}"\n'%(ip,mask))
        #downfile.write('route delete %s/%s ${OLDGW}\n'%(ip,mask))

    #downfile.write('\n\nrm /tmp/pptp_oldgw\n')
    upfile.close()
    #downfile.close()

    #print "For pptp on mac only, please copy ip-up and ip-down to the /etc/ppp folder," \
    #      "don't forget to make them executable with the chmod command."
    return

def generate_win(metric):
    global d3,day,results
    fetch_ip_data()
    if d3<day:return

    upscript_header=textwrap.dedent("""@echo off
set path=%path%;%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem;"%~dp0";"%cd:"=%"
set ERRORLEVEL=
pushd "%~dp0"

title VPN智能路由开启
echo 正在查询当前网关，请稍候
setlocal EnableDelayedExpansion
for /F "tokens=3,4" %%i in ('route print ^| findstr "\<0.0.0.0\>"') do (set "gw=%%i"&(if "!gw:.=!"=="!gw!" set "gw=%%j")&(if "!gwf!"=="" set "gwf=%%i"&set "iof=%%j"))
if "!iof:.=!"=="!iof!" set "iof=none"
if "!gwf:.=!"=="!gwf!" set "gwf=none"
if "!gwf:.=!"=="!gwf!" if not "!iof!"=="none" set "gwf=!iof!"
rem echo %iof%
rem echo %gw% >>gw.txt
rem if not "!gwf!"=="none" echo %gwf% >>gw.txt
echo 当前网关:%gw%
echo 原网关:%gwf%
echo 接下来将开启智能路由
echo 注意需要以管理员身份运行
if not "%~1"=="-s" pause
rem tracert 183.60.45.20
rem route print
rem ipconfig /flushdns

rem set gwl=%gw%
rem set gwl=192.168.2.1
rem route CHANGE 0.0.0.0 mask 0.0.0.0 %gwl% metric 1
rem route CHANGE 192.168.5.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.1.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.2.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.137.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.3.0 mask 255.255.255.0 %gw% metric 1

ipconfig /flushdns >nul
rem if not "!gwf!"=="none" if not "!iof!"=="none" route CHANGE 0.0.0.0 mask 0.0.0.0 %gwf% metric 4265
rem if not "!gwf!"=="none" if not "!iof!"=="none" route CHANGE 0.0.0.0 mask 0.0.0.0 %gwf% metric 20
if not "!gwf!"=="none" set "gw=!fwf!"

    """)

    upscript_footer=textwrap.dedent("""

ipconfig /flushdns >nul
echo 开启完毕!
rem if not "%~1"=="-s" pause>nul
popd
exit

:rt
route CHANGE %* 2>nul
route add %* 2>nul
goto :EOF

    """)

    upfile=open('vpnup-win.bat','w')
    #downfile=open('vpndown-win.bat','w')

    upfile.write(upscript_header)
    #upfile.write('\n')
    #upfile.write('ipconfig /flushdns >nul\n\n')
    if not ng=='192.168.2.1':
        upfile.write('set "gw=%s"\n\n'%(ng))

    #downfile.write("@echo off")
    #downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('call :rt %s mask %s %s metric %d\n'%(ip,mask,"%gw%",metric))
        #downfile.write('route delete %s\n'%(ip))

    upfile.write(upscript_footer)
    upfile.close()
    #downfile.close()
    generate_winp(args.metric)
    generate_winfc(args.metric)

#    up_vbs_wrapper=open('vpnup.vbs','w')
#    up_vbs_wrapper.write('Set objShell = CreateObject("Wscript.shell")\ncall objShell.Run("vpnup.bat",0,FALSE)')
#    up_vbs_wrapper.close()
#    down_vbs_wrapper=open('vpndown.vbs','w')
#    down_vbs_wrapper.write('Set objShell = CreateObject("Wscript.shell")\ncall objShell.Run("vpndown.bat",0,FALSE)')
#    down_vbs_wrapper.close()

    #print "For pptp on windows only, run vpnup.bat before dialing to vpn," \
    #      "and run vpndown.bat after disconnected from the vpn."
    return

def generate_winp(metric):
    global d3,day,results
    fetch_ip_data()
    if d3<day:return

    upscript_header=textwrap.dedent("""@echo off
set path=%path%;%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem;"%~dp0";"%cd:"=%"
set ERRORLEVEL=
pushd "%~dp0"

title VPN智能路由开启
echo 正在查询当前网关，请稍候
setlocal EnableDelayedExpansion
for /F "tokens=3,4" %%i in ('route print ^| findstr "\<0.0.0.0\>"') do (set "gw=%%i"&(if "!gw:.=!"=="!gw!" set "gw=%%j")&(if "!gwf!"=="" set "gwf=%%i"&set "iof=%%j"))
if "!iof:.=!"=="!iof!" set "iof=none"
if "!gwf:.=!"=="!gwf!" set "gwf=none"
if "!gwf:.=!"=="!gwf!" if not "!iof!"=="none" set "gwf=!iof!"
rem echo %iof%
rem echo %gw% >>gw.txt
rem if not "!gwf!"=="none" echo %gwf% >>gw.txt
echo 当前网关:%gw%
echo 原网关:%gwf%
echo 接下来将开启智能路由
echo 注意需要以管理员身份运行
if not "%~1"=="-s" pause
rem tracert 183.60.45.20
rem route print
rem ipconfig /flushdns

rem set gwl=%gw%
rem set gwl=192.168.2.1
rem route CHANGE 0.0.0.0 mask 0.0.0.0 %gwl% metric 1
rem route CHANGE 192.168.5.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.1.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.2.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.137.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.3.0 mask 255.255.255.0 %gw% metric 1

ipconfig /flushdns >nul
rem if not "!gwf!"=="none" if not "!iof!"=="none" route CHANGE 0.0.0.0 mask 0.0.0.0 %gwf% metric 4265
rem if not "!gwf!"=="none" if not "!iof!"=="none" route CHANGE 0.0.0.0 mask 0.0.0.0 %gwf% metric 20
if not "!gwf!"=="none" set "gw=!fwf!"

    """)

    upscript_footer=textwrap.dedent("""

ipconfig /flushdns >nul
echo 开启完毕!
rem if not "%~1"=="-s" pause>nul
popd
exit

:rt
route CHANGE %* 2>nul
route -p add %* 2>nul
goto :EOF

    """)

    upfile=open('vpnup-winp.bat','w')
    #downfile=open('vpndown-winp.bat','w')

    upfile.write(upscript_header)
    #upfile.write('\n')
    #upfile.write('ipconfig /flushdns >nul\n\n')
    if not ng=='192.168.2.1':
        upfile.write('set "gw=%s"\n\n'%(ng))

    #downfile.write("@echo off")
    #downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('call :rt %s mask %s %s metric %d\n'%(ip,mask,"%gw%",metric))
        #downfile.write('route delete %s\n'%(ip))

    upfile.write(upscript_footer)
    upfile.close()
    #downfile.close()
    #generate_winfc(args.metric)

#    up_vbs_wrapper=open('vpnup.vbs','w')
#    up_vbs_wrapper.write('Set objShell = CreateObject("Wscript.shell")\ncall objShell.Run("vpnup.bat",0,FALSE)')
#    up_vbs_wrapper.close()
#    down_vbs_wrapper=open('vpndown.vbs','w')
#    down_vbs_wrapper.write('Set objShell = CreateObject("Wscript.shell")\ncall objShell.Run("vpndown.bat",0,FALSE)')
#    down_vbs_wrapper.close()

    #print "For pptp on windows only, run vpnup.bat before dialing to vpn," \
    #      "and run vpndown.bat after disconnected from the vpn."
    return

def generate_winfc(metric):
    global d3,day,results
    fetch_ip_data()
    if d3<day:return

    upscript_header=textwrap.dedent("""[加速模式]
海外加速=MeToLocalGW
全部加速=AllToRemoteGW

[加速模式说明]
海外加速=只是访问国外站点的流量经过VPN,访问国内快。
全部加速=所有网络的流量都经过VPN，办公室上淘宝，QQ。

[海外加速]
    """)

    upfile=open('route.dat','w')

    upfile.write(upscript_header)
    #upfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('%s=%s\n'%(ip,mask))

    upfile.close()
    return

def generate_android(metric):
    global d3,day,results
    fetch_ip_data()
    if d3<day:return

    upscript_header=textwrap.dedent("""\
#!/bin/sh
alias nestat='/system/xbin/busybox netstat'
alias grep='/system/xbin/busybox grep'
alias awk='/system/xbin/busybox awk'
alias route='/system/xbin/busybox route'

OLDGW=`netstat -rn | grep ^0\.0\.0\.0 | awk '{print $2}'`
#OLDGW='192.168.2.1'

    """)

    downscript_header=textwrap.dedent("""\
#!/bin/sh
alias route='/system/xbin/busybox route'

    """)

    upfile=open('vpnup_android.sh','w')
    #downfile=open('vpndown_android.sh','w')

    upfile.write(upscript_header)
    upfile.write('\n')
    #downfile.write(downscript_header)
    #downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('route add -net %s netmask %s gw $OLDGW\n'%(ip,mask))
        #downfile.write('route del -net %s netmask %s\n'%(ip,mask))

    upfile.close()
    #downfile.close()

    #print "Old school way to call up/down script from openvpn client. " \
    #      "use the regular openvpn 2.1 method to add routes if it's possible"
    return

def fetch_ip_data():
    global n,results,test,d3,day
    if not os.path.exists('test.txt'):
        d3=8
        day=0
    if d3<day:
        test=1
        if n==0:print 'no need to update.'
        n=1
    if n==1:return results
    n=1
    #fetch data from apnic
    print "Fetching data from apnic.net, it might take a few minutes, please wait..."
    if not test==1 or not os.path.exists('test.txt'):
        if(sysstr =="Windows"):
            if os.path.exists('wget.exe'):os.system("wget --no-check-certificate -c http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O test.txt")
            else:
                url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
                data=urllib2.urlopen(url).read()
                open('test.txt','w').write(data)
        elif(sysstr =="Linux"):
            os.system("wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O test.txt")
        else:
            url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
            data=urllib2.urlopen(url).read()
            open('test.txt','w').write(data)
    data=open('test.txt').read()
    #print data

    cnregex=re.compile(r'apnic\|cn\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',re.IGNORECASE)
    cndata=cnregex.findall(data)

    #print cndata
    for item in cndata:
        unit_items=item.split('|')
        starting_ip=unit_items[3]
        num_ip=int(unit_items[4])

        imask=0xffffffff^(num_ip-1)
        #convert to string
        imask=hex(imask)[2:]
        mask=[0]*4
        mask[0]=imask[0:2]
        mask[1]=imask[2:4]
        mask[2]=imask[4:6]
        mask[3]=imask[6:8]

        #convert str to int
        mask=[ int(i,16 ) for i in mask]
        mask="%d.%d.%d.%d"%tuple(mask)

        #mask in *nix format
        mask2=32-int(math.log(num_ip,2))

        #print starting_ip,mask,mask2
        results.append((starting_ip,mask,mask2))

    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description="Generate routing rules for vpn.-p -m -d -t -g -x")
    parser.add_argument('-p','--platform',
                        dest='platform',
                        default='auto',
                        nargs='?',
                        help="Target platforms, it can be openvpn, ovpn, mac, linux,"
                        "win, winp, android, pac, all,auto. all by default.")
    parser.add_argument('-m','--metric',
                        dest='metric',
                        default=5,
                        nargs='?',
                        type=int,
                        help="Metric setting for the route rules")
    parser.add_argument('-d','--day',
                        dest='day',
                        default=7,
                        nargs='?',
                        type=int,
                        help="How many days for update.")
    parser.add_argument('-t','--test',
                        dest='test',
                        default=0,
                        nargs='?',
                        type=int,
                        help="test mode,no download.")
    parser.add_argument('-g','--gate',
                        dest='ng',
                        default='192.168.2.1',
                        nargs='?',
                        help="Set GateWay.")

    parser.add_argument('-x', '--proxy',
                        dest    = 'proxy',
                        default = 'PROXY 192.168.2.1:8118;PROXY 192.168.2.1:8087;PROXY 127.0.0.1:8087;PROXY 127.0.0.1:8118;SOCKS5 192.168.2.1:1080;SOCKS5 127.0.0.1:1080;SOCKS5 127.0.0.1:48102;SOCKS5 127.0.0.1:65500;SOCKS5 127.0.0.1:7070;DIRECT',
                        nargs   = '?',
                        help    = "Proxy Server, examples: "
                                  "SOCKS5 127.0.0.1:8964; "
                                  "SOCKS 127.0.0.1:8964; "
                                  "PROXY 127.0.0.1:6489")

    args = parser.parse_args()

    if args.day!=7:day=args.day
    if args.metric!=5:metric=args.metric
    if args.test!=0:test=args.test
    if args.ng!='':ng=args.ng.replace('\'','')
    if args.platform.lower() == 'openvpn':
        generate_ovpn(args.metric)
    elif args.platform.lower() == 'linux':
        generate_linux(args.metric)
    elif args.platform.lower() == 'mac':
        generate_mac(args.metric)
    elif args.platform.lower() == 'win':
        generate_win(args.metric)
    elif args.platform.lower() == 'winp':
        generate_winp(args.metric)
    elif args.platform.lower() == 'winfc':
        generate_winfc(args.metric)
    elif args.platform.lower() == 'android':
        generate_android(args.metric)
    elif args.platform.lower() == 'pac':
        generate_pac(args.proxy)
    elif args.platform.lower() == 'all':
        generate_ovpn(args.metric)
        generate_linux(args.metric)
        generate_mac(args.metric)
        generate_win(args.metric)
        #generate_winp(args.metric)
        generate_android(args.metric)
        generate_pac(args.proxy)
    elif args.platform.lower() == 'auto':
        #print sysstr
        generate_ovpn(args.metric)
        generate_pac(args.proxy)
        if(sysstr =="Windows"):
            #print ("Call Windows tasks")
            generate_win(args.metric)
            #generate_winp(args.metric)
        elif(sysstr == "Linux"):
            #print ("Call Linux tasks")
            if 'SMP' in platform.version():
                generate_android(args.metric)
            else:
                generate_linux(args.metric)
        else:
            #print ("Other System tasks")
            generate_mac(args.metric)
    else:
        print>>sys.stderr, "Platform %s is not supported."%args.platform
        exit(1)

