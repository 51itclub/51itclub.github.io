#!/usr/bin/env python
# Flora_Pac by @leaskh
# www.leaskh.com, i@leaskh.com
# Optimized by @yaleh
# Based on chnroutes project (by Numb.Majority@gmail.com)

import re
import urllib2
import argparse
import math
import ipaddress

# tunable with primes for balancing of matching times and code size
# increase it for better performance
# decrease it for smaller size
global HASH_BASE, MASK_STEP, min_prefixlen, max_prefixlen

HASH_BASE = 3011
MASK_STEP = 2

min_prefixlen = 32
max_prefixlen = 0

def generate_balanced_proxy(proxies, balance):
    if balance == 'no':
        return "return '%s' ;" % (';'.join(proxies))
    elif balance == 'local_ip':
        return '''
  var local_ip_balance = function(proxies) {
    var i, k, l, myseg, s, _i;
    myseg = parseInt(myIpAddress().split(".")[3]);
    l = proxies.length;
    k = myseg % l;
    s = '';
    for (i = _i = 0; 0 <= l ? _i < l : _i > l; i = 0 <= l ? ++_i : --_i) {
      s += proxies[(k + i) % l];
    }
    return s;
  };
''' + """
  return local_ip_balance([%s]);
""" % (','.join(map(lambda p: "'%s'" % p, proxies)))
    elif balance == 'host':
        return '''
  var target_host_balance = function(proxies, host) {
    var hash_string, i, k, l, s, _i;
    hash_string = function(s) {
      var c, hash, _i, _len;
      hash = 0;
      for (_i = 0, _len = s.length; _i < _len; _i++) {
        c = s[_i];
        hash = (hash << 5) - hash + c.charCodeAt(0);
        hash = hash & hash & 0xFFFF;
        hash &= 0xFFFF;
      }
      return hash;
    };
    l = proxies.length;
    k = hash_string(host) % l;
    s = '';
    for (i = _i = 0; 0 <= l ? _i < l : _i > l; i = 0 <= l ? ++_i : --_i) {
      s += proxies[(k + i) % l];
    }
    return s;
  };
''' + """
  return target_host_balance([%s], host);
""" % (','.join(map(lambda p: "'%s'" % p, proxies)))

def generate_no_proxy(no_proxy):
    s = ''
    for n in no_proxy:
        try:
            # single IP address
            ip = ipaddress.ip_address(u"%s" % n)
            s += " ip == '%s' ||" % n
            continue;
        except ValueError:
            pass
        
        try:
            # network with mask or mask prefix 
            net = ipaddress.ip_network(u"%s" % n)
            s += " isInNet(ip, '%s', '%s') ||" % (net.network_address, net.netmask)
            continue
        except ValueError:
            pass

        # hostname
        s += " host == '%s' ||" % n

    return s

def generate_pac(proxies, balance, no_proxy):
    # TODOs: fregment net, save prefix/24 to a 2D array with the 1st-D index of a mod-x key

    results  = merge_all(fetch_ip_data())

    for net in results:
        global min_prefixlen, max_prefixlen
        i = net.prefixlen
        if i < min_prefixlen:
            min_prefixlen = i
        if i > max_prefixlen:
            max_prefixlen = i

    print "PrefixLen: [%d, %d]" % (min_prefixlen, max_prefixlen)
 
#    print "Hashing...\n"
    hashed_results = hash_nets(fregment_nets(results), HASH_BASE)

    pacfile  = 'flora_pac_yaleh_mod.pac'
    rfile    = open(pacfile, 'w')
    strLines = ("""
// Flora_Pac by @leaskh
// www.leaskh.com, i@leaskh.com
// Optimized by @yaleh
   
function FindProxyForURL(url, host) {
  var HASH_BASE, MASK_STEP, a, dot2num, hash_masked_ip, hashed_nets, i, lookup_ip, max_prefixlen, min_prefixlen, num2dot, prefixlen2mask, rebuild_net, _i, _j, _len, _len1;

  dot2num = function(dot) {
    var d;
    d = dot.split(".");
    return ((((((+d[0]) * 256) + (+d[1])) * 256) + (+d[2])) * 256) + (+d[3]);
  };

  num2dot = function(ip) {
    return [ip >>> 24, ip >>> 16 & 0xFF, ip >>> 8 & 0xFF, ip & 0xFF].join(".");
  };

  hash_masked_ip = function(ip, mask_len, mod_base) {
    var i, net, offset, _i;
    offset = 32 - mask_len;
    net = ip >>> offset;
    for (i = _i = 0; 0 <= offset ? _i < offset : _i > offset; i = 0 <= offset ? ++_i : --_i) {
      net *= 2;
    }
    return net % mod_base;
  };

  prefixlen2mask = function(prefixlen) {
    var imask;
    imask = 0xFFFFFFFF << (32 - prefixlen);
    return (imask >> 24 & 0xFF) + '.' + (imask >> 16 & 0xFF) + '.' + (imask >> 8 & 0xFF) + '.' + (imask & 0xFF);
  };

  rebuild_net = function(pair) {
    var masks, result;
    result = ['', ''];
    result[0] = num2dot(pair[0] << (32 - pair[1]));
    result[1] = prefixlen2mask(pair[1]);
    return result;
  };

  lookup_ip = function(ip) {
    var i, k, len, n, n_ip, _i, _len, _ref;
    len = min_prefixlen;
    n_ip = dot2num(ip);
    while (len <= max_prefixlen) {
      k = hash_masked_ip(n_ip, len, HASH_BASE);
      _ref = hashed_nets[k];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        i = _ref[_i];
        n = rebuild_net(i);
        if (isInNet(ip,n[0],n[1])) {
          return true;
        }
      }
      len += MASK_STEP;
    }
    return false;
  };
"""
    )
    strLines += """

  HASH_BASE = %d;
  MASK_STEP = %d;
  min_prefixlen = %d;
  max_prefixlen = %d;

""" % (HASH_BASE, MASK_STEP, min_prefixlen, max_prefixlen)

    intLines = 0

    for i in xrange(min_prefixlen, max_prefixlen+1, MASK_STEP):
        strLines +="""
    var m%d = %d;
""" % (i, i)

    strLines += """
    var empty_array = [];
    var hashed_nets = [
"""
    none_empty_count = 0
    for i in range(len(hashed_results)):
#        print "%d: %d" % (i, len(hashed_results[i]))
        if len(hashed_results[i]) > 0:
            none_empty_count += 1
            strLines += "\n        ["
            for net in hashed_results[i]:
                strLines += "\n            [%d, m%d]," % (int(net.network_address) >> (32 - net.prefixlen),
                                                         net.prefixlen)
            strLines += "\n        ],"
        else:
            strLines += "\n        empty_array,"
    avg_len = float(len(results)) / none_empty_count
    print "Avarage matching length: %f" % avg_len
    steps = (max_prefixlen - min_prefixlen) / MASK_STEP + 1
    print "Steps to match: %d" % steps
    print "Matching cost est.: %f" % (avg_len * steps)
    strLines = strLines + ("""
    ];

    if (isPlainHostName(host)
     || (host == '127.0.0.1')
     || (host == 'localhost')
     ) {
        return 'DIRECT';
    }

    var ip = dnsResolve(host);

    if (ip == null || ip == '' || %s lookup_ip(ip)) {
        return 'DIRECT';
    }

    %s

}
""" % (generate_no_proxy(no_proxy), generate_balanced_proxy(proxies, balance)))
    rfile.write(strLines)
    rfile.close()
    print ("Rules: %d items.\n"
           "Usage: Use the newly created %s as your web browser's automatic "
           "proxy configuration (.pac) file."%(intLines, pacfile))

def merge_nets(net1, net2):
    super_net1 = net1.supernet()
    super_net2 = net2.supernet()

    if super_net1 == super_net2 \
            and super_net1.network_address == net1.network_address \
            and super_net1.broadcast_address == net2.broadcast_address:
        return super_net1

    return None

def merge_all(networks):
    i = 1
    while i < len(networks):
        if i == 0:
            i += 1
            continue
        merged_net = merge_nets(networks[i-1], networks[i])
        if merged_net is None:
            i += 1
            continue
        networks[i-1] = merged_net
        networks.pop(i)
        if i > 1:
            i -= 1

    return networks

def fregment_net(net):
    # return networks of mask 4, 8, 12, 16, 20, 24
#    print "Fregment %s" % str(net)
    subnets = []
    target_prefixlen = (net.prefixlen - 1) / MASK_STEP * MASK_STEP + MASK_STEP
    for a in net.subnets(target_prefixlen - net.prefixlen):
        subnets.append(a)

    return subnets

def fregment_nets(nets):
    results = []
    for net in nets:
        results += fregment_net(net)
    return results

def hash_address(address, mod_base):
#    print "Hash %s" % str(address)
    return int(address) % mod_base

def hash_nets(nets, mod_base):
    hashed = [[] for i in range(mod_base)]
    for net in nets:
        i = hash_address(net.network_address, mod_base)
        hashed[i].append(net)
    return hashed

def fetch_ip_data():
    #fetch data from apnic
    print "Fetching data from apnic.net, it might take a few minutes, please wait..."
    url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    data=urllib2.urlopen(url).read()

    cnregex=re.compile(r'apnic\|cn\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',re.IGNORECASE)
    cndata=cnregex.findall(data)

    results=[]

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

        net = ipaddress.ip_network(u"%s/%s" % (starting_ip, mask))

        results.append(net)

    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description="Generate proxy auto-config rules.")
    parser.add_argument('-x', '--proxy',
                        dest = 'proxy',
                        default = ['PROXY 192.168.2.1:8118;PROXY 192.168.2.1:8087;PROXY 127.0.0.1:8087;PROXY 127.0.0.1:8118;SOCKS5 192.168.2.1:1080;SOCKS5 127.0.0.1:1080;SOCKS5 127.0.0.1:48102;SOCKS5 127.0.0.1:65500;SOCKS5 127.0.0.1:7070;DIRECT'],
                        nargs = '*',
                        help = "Proxy Server, accepts multple values for balancing, i.e.: "
                               "-x 'SOCKS 127.0.0.1:8964' 'SOCKS5 127.0.0.1:1984' 'PROXY 127.0.0.1:1989'")
    parser.add_argument('-m', '--mask-step',
                        type = int,
                        dest = 'mask_step',
                        default = 2,
                        help = "Step size of mask fregment (default: %(default)s)")
    parser.add_argument('-s', '--hash-base',
                        type = int,
                        dest = 'hash_base',
                        default = 3011,
                        help = 'Size of the address hash table (default: %(default)s)')
    parser.add_argument("-b", '--balance',
                        choices=["no", "local_ip", "host"],
                        dest = 'balance',
                        default = "no",
                        help = "Balancing policy: "
                               "'no' for no balancing, "
                               "'local_ip' for balancing by local IP, "
                               "'host' for balancing by Web site's hostname "
                               "(default: %(default)s)")
    parser.add_argument('-n', '--no-proxy',
                        dest = 'no_proxy',
                        nargs = '*',
                        default = ['192.168.0.0/24'],
                        help = "Don't proxy request to the specified IP or network, i.e.: "
                               "'192.168.0.0/24' '172.16.0.0/255.255.0.0 ' . "
                               "(default: %(default)s)")

    args = parser.parse_args()
#    global HASH_BASE, MASK_STEP
    HASH_BASE = args.hash_base
    MASK_STEP = args.mask_step

#    for p in args.proxy:
#        print p
    generate_pac(args.proxy, args.balance, args.no_proxy)
