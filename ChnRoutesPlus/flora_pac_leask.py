#!/usr/bin/env python
# Flora_Pac by @leaskh
# www.leaskh.com, i@leaskh.com
# Based on chnroutes project (by Numb.Majority@gmail.com)

import re
import urllib2
import argparse
import math
import socket
import struct


def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


def generate_pac(proxy):
    results  = fetch_ip_data()
    pacfile  = 'flora_pac.pac'
    rfile    = open(pacfile, 'w')
    results.insert(0, (ip2long('127.0.0.1'),   ip2long('255.0.0.0'),   0))
    results.insert(1, (ip2long('10.0.0.0'),    ip2long('255.0.0.0'),   0))
    results.insert(2, (ip2long('172.16.0.0'),  ip2long('255.240.0.0'), 0))
    results.insert(3, (ip2long('192.168.0.0'), ip2long('255.255.0.0'), 0))

    def ip(item):
        return item[0]

    results = sorted(results, key = ip)

    strLines = """// Flora_Pac by @leaskh
// www.leaskh.com, i@leaskh.com

function FindProxyForURL(url, host) {

    var list = ["""
    intLines = 0
    for ip,mask,_ in results:
        if intLines > 0:
            strLines = strLines + ','
        intLines = intLines + 1
        strLines = strLines + """
        [%d, %d]"""%(ip, mask)
    strLines = strLines + """
    ];

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

    var dangerDomains = {
     // 'apple.com' : 1,
        'google.com' : 1,
        'twitter.com' : 1,
        'facebook.com' : 1,
        'yyets.com' : 1,
        'tw.yahoo.com' : 1,
        'youtube.com' : 1,
        'zaobao.com.sg' : 1
    };

    // see https://github.com/clowwindy/ChinaDNS/blob/master/chinadns/dnsrelay.py
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
        3478  : 1,
        3479  : 1,
        3480  : 1,
        3481  : 1,
        3482  : 1,
        3483  : 1,
        3484  : 1,
        3485  : 1,
        3486  : 1,
        3487  : 1,
        3488  : 1,
        3489  : 1,
        3490  : 1,
        3491  : 1,
        3492  : 1,
        3493  : 1,
        3494  : 1,
        3495  : 1,
        3496  : 1,
        3497  : 1,
        16384 : 1,
        16385 : 1,
        16386 : 1,
        16387 : 1,
        16393 : 1,
        16394 : 1,
        16395 : 1,
        16396 : 1,
        16397 : 1,
        16398 : 1,
        16399 : 1,
        16400 : 1,
        16401 : 1,
        16402 : 1
    };

    var proxy = '%s';

    function convertAddress(ipchars) {
        var bytes = ipchars.split('.');
        var result = ((bytes[0] & 0xff) << 24) |
                     ((bytes[1] & 0xff) << 16) |
                     ((bytes[2] & 0xff) <<  8) |
                      (bytes[3] & 0xff);
        return result;
    }

    function match(ip, list) {
        var left = 0, right = list.length;
        do {
            var mid = Math.floor((left + right) / 2),
                ipf = (ip & list[mid][1]) >>> 0,
                m   = (list[mid][0] & list[mid][1]) >>> 0;
            if (ipf == m) {
                return true;
            } else if (ipf > m) {
                left  = mid + 1;
            } else {
                right = mid;
            }
        } while (left + 1 <= right)
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

    // fix error message in FoxyProxy when switching tabs. http://verihy.me/posts/foxyproxy-pac/
    if (typeof host === 'undefined'
     || isPlainHostName(host)
     || host === '127.0.0.1'
     || host === 'localhost') {
        return 'DIRECT';
    }

    if (testDomain(host, safeDomains, true)) {
        return 'DIRECT';
    }

    if (testDomain(host, dangerDomains)) {
        return proxy;
    }

    if (safePorts[host.split(':')[1]]) {
        return 'DIRECT';
    }

    var strIp = dnsResolve(host);
    if (!strIp) {
        return proxy;
    }

    if (fakeIps[strIp]) {
        return proxy;
    }

    var intIp = convertAddress(strIp);
    if (match(intIp, list)) {
        return 'DIRECT';
    }

    return proxy;

}
"""%(proxy)
    rfile.write(strLines)
    rfile.close()
    print ("Rules: %d items.\n"
           "Usage: Use the newly created %s as your web browser's automatic "
           "PAC(Proxy auto-config) file."%(intLines, pacfile))


def pac_server(port):
    if port <= 0:
        return
    import SimpleHTTPServer
    import BaseHTTPServer
    class DefaultHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/flora_pac.pac'
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), DefaultHandler)
    print "PAC is now serving at: 0.0.0.0:%d"%(port)
    print "Check it out with: $ curl http://127.0.0.1:%d"%(port)
    httpd.serve_forever()


def fetch_ip_data():
    #fetch data from apnic
    print "Fetching data from apnic.net, it might take a few minutes, please wait..."
    url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
  # url=r'http://flora/delegated-apnic-latest' #debug
    data=urllib2.urlopen(url).read()

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate proxy auto-config rules.")
    parser.add_argument('-x', '--proxy',
                        dest    = 'proxy',
                        default = 'SOCKS5 127.0.0.1:8964; SOCKS 127.0.0.1:8964; DIRECT',
                        nargs   = '?',
                        help    = "Proxy Server, examples: "
                                  "SOCKS5 127.0.0.1:8964; "
                                  "SOCKS 127.0.0.1:8964; "
                                  "PROXY 127.0.0.1:6489")
    parser.add_argument('-p', '--port',
                        dest    = 'port',
                        default = '0',
                        nargs   = '?',
                        help    = "Pac Server Port [OPTIONAL], examples: 8970")
    args = parser.parse_args()
    generate_pac(args.proxy)
    pac_server(int(args.port))
