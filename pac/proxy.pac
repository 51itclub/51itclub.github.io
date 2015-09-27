//    http://dwz.cn/1N9nW7
//    http://flora.leaskh.com/pac?proxy=PROXY%20192.168.2.1%3A8118%3BPROXY%20192.168.2.1%3A8087%3BPROXY%20127.0.0.1%3A8087%3BPROXY%20127.0.0.1%3A8118%3BSOCKS5%20192.168.2.1%3A1080%3BSOCKS5%20127.0.0.1%3A1080%3BSOCKS5%20127.0.0.1%3A48102%3BSOCKS5%20127.0.0.1%3A65500%3BSOCKS5%20127.0.0.1%3A7070%3BDIRECT
//    http://dwz.cn/1MiXrt
//    http://flora.leaskh.com/pac?proxy=PROXY%20127.0.0.1%3A8118%3B%20SOCKS5%20127.0.0.1%3A1080%3B%20SOCKS%20127.0.0.1%3A1080%3B%20SOCKS5%20127.0.0.1%3A48102%3B%20SOCKS5%20127.0.0.1%3A65500%3B%20SOCKS5%20127.0.0.1%3A7070%3B%20PROXY%20127.0.0.1%3A8087%3B%20SOCKS5%20192.168.2.1%3A1080%3B%20PROXY%20127.0.0.1%3A8080%3B%20SOCKS5%20127.0.0.1%3A1081
//IPV4 TO IPV6:http://www.subnetonline.com/pages/subnet-calculators/ipv4-to-ipv6-converter.php
//IPV6地址加端口表示方法http://desert3.iteye.com/blog/1595253

//-----------------------------------------------------------------
var hasOwnProperty = Object.hasOwnProperty;
var extend=function(o,n,override){for(var p in n)if(n.hasOwnProperty(p) && (!o.hasOwnProperty(p) || override))o[p]=n[p];for(var p in o)n[p]=o[p]};

var direct = "DIRECT";
var wall_proxy = function(){ return "__PROXY__;PROXY 192.168.2.1:8118;PROXY 192.168.2.1:8087;PROXY 127.0.0.1:8087;PROXY 127.0.0.1:8118;SOCKS5 192.168.2.1:1080;SOCKS5 127.0.0.1:1080;SOCKS5 127.0.0.1:48102;SOCKS5 127.0.0.1:65500;SOCKS5 127.0.0.1:7070;" + direct; };
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

var list = [
    [16777216, 4294901760],
    [16842752, 4294901760],
    [16908288, 4294901760],
    [16973824, 4294901760],
    [17039360, 4294901760],
    [3757572096, 4294705152],
    [3757834240, 4294901760],
    [3757965312, 4294901760],
    [3758030848, 4294901760]
];

//----------------以下是需要屏蔽的host主机网址-----------------------

var blackhole_host = {
    'www.36595501.com': 1,
    '118.26.200.246': 1,
    '122.227.254.195': 1,
};

var dangerDomains = {
    'www.36595501.com' : 1,
    'wap.jrnapkin.cn' : 1,
};


//----------------以下是确认需要翻墙的host主机网址----------------------

var domains = {
  "gimpshop.com": 1,
  "directcreative.com": 1,
  "speedpluss.org": 1,
  "mingpaovan.com": 1,
  "1-apple.com.tw": 1
};

var autoproxy_host = {
    "0rz.tw": 1,
    "0to255.com": 1,
    "1-apple.com.tw": 1,
    "10musume.com": 1,
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
    '122.227.254.195': 1,
};


//----------------以下是对象合并、选择和处理-----------------------

//var o1={hello:1},o2={world:2};
//extend(o1,o2);
extend(autoproxy_host,domains);
extend(dangerDomains,blackhole_host);
var autoproxy_host = domains   //以domains为准
//var domains = autoproxy_host   //以autoproxy_host为准
var dangerDomains = blackhole_host  //以blackhole_host为准
//var blackhole_host = dangerDomains  //以dangerDomains为准
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
    do {
        if (autoproxy_host.hasOwnProperty(host)) {
            return wall_proxy();
        }
        lastPos = host.indexOf('.') + 1;
        host = host.slice(lastPos);
    } while (lastPos >= 1);
    var strIp = dnsResolve(host);
    if ( !strIp ) {
        return wall_proxy();
    } else { return getProxyFromIP(strIp); }
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
            return true;
            //return i;
        } else {
            return false;
        }
    }
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
    if ( isInSubnetRange(subnetIpRangeList, intIp) ) {
        return direct;
    }
    var index = ((intIp & 0xff000000) >>> 0 ) % 255;
    if (match(intIp, list[index])) {
        return direct;
    }
    return wall_proxy();
}



//-----------------------------------------------------------------


function FindProxyForURL_BAK1(url, host) {
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
function FindProxyForURLEx_BAK1(url, host) {
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
    //return hostindomainsex(blackhole_host, host);
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
    //return gfwed[host2domain(host)] ? http_proxy : direct;
    //return hostindomainsex(blackhole_host, host);
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





