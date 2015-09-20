#!/usr/bin/env python
#coding=gbk

#Modified by 51itclub,welcome to my site:51itclub.net


test=0
day=7
metric=5
ng=''

















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
    global d3,day
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
    downfile=open('vpndown_linux.sh','w')

    upfile.write(upscript_header)
    upfile.write('\n')
    downfile.write(downscript_header)
    downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('route add -net %s netmask %s gw $OLDGW\n'%(ip,mask))
        downfile.write('route del -net %s netmask %s\n'%(ip,mask))

    upfile.close()
    downfile.close()

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
    downfile=open('ip-down_linux','w')

    upfile.write(upscript_header)
    upfile.write('\n')
    downfile.write(downscript_header)
    downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('route add -net %s netmask %s gw $OLDGW\n'%(ip,mask))
        downfile.write('route del -net %s netmask %s\n'%(ip,mask))

    downfile.write('rm /tmp/vpn_oldgw\n')

    #print "For pptp only, please copy the file ip-pre-up to the folder/etc/ppp," \
    #      "and copy the file ip-down to the folder /etc/ppp/ip-down.d."
    return

def generate_mac(metric):
    global d3,day
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
    downfile=open('ip-down_mac','w')


    upfile.write(upscript_header)
    upfile.write('\n')
    downfile.write(downscript_header)
    downfile.write('\n')

    for ip,_,mask in results:
        upfile.write('route add %s/%s "${OLDGW}"\n'%(ip,mask))
        downfile.write('route delete %s/%s ${OLDGW}\n'%(ip,mask))

    downfile.write('\n\nrm /tmp/pptp_oldgw\n')
    upfile.close()
    downfile.close()

    #print "For pptp on mac only, please copy ip-up and ip-down to the /etc/ppp folder," \
    #      "don't forget to make them executable with the chmod command."
    return

def generate_win(metric):
    global d3,day
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
pause
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
rem pause>nul
popd
exit

:rt
route CHANGE %* 2>nul
route add %* 2>nul
goto :EOF

    """)

    upfile=open('vpnup-win.bat','w')
    downfile=open('vpndown-win.bat','w')

    upfile.write(upscript_header)
    #upfile.write('\n')
    #upfile.write('ipconfig /flushdns >nul\n\n')
    if not ng=='192.168.2.1':
        upfile.write('set "gw=%s"\n\n'%(ng))

    downfile.write("@echo off")
    downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('call :rt %s mask %s %s metric %d\n'%(ip,mask,"%gw%",metric))
        downfile.write('route delete %s\n'%(ip))

    upfile.write(upscript_footer)
    upfile.close()
    downfile.close()
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
    global d3,day
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
pause
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
rem pause>nul
popd
exit

:rt
route CHANGE %* 2>nul
route -p add %* 2>nul
goto :EOF

    """)

    upfile=open('vpnup-winp.bat','w')
    downfile=open('vpndown-winp.bat','w')

    upfile.write(upscript_header)
    #upfile.write('\n')
    #upfile.write('ipconfig /flushdns >nul\n\n')
    if not ng=='192.168.2.1':
        upfile.write('set "gw=%s"\n\n'%(ng))

    downfile.write("@echo off")
    downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('call :rt %s mask %s %s metric %d\n'%(ip,mask,"%gw%",metric))
        downfile.write('route delete %s\n'%(ip))

    upfile.write(upscript_footer)
    upfile.close()
    downfile.close()
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
    global d3,day
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
    global d3,day
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
    downfile=open('vpndown_android.sh','w')

    upfile.write(upscript_header)
    upfile.write('\n')
    downfile.write(downscript_header)
    downfile.write('\n')

    for ip,mask,_ in results:
        upfile.write('route add -net %s netmask %s gw $OLDGW\n'%(ip,mask))
        downfile.write('route del -net %s netmask %s\n'%(ip,mask))

    upfile.close()
    downfile.close()

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
    if n==1:return
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

    return


if __name__=='__main__':
    parser=argparse.ArgumentParser(description="Generate routing rules for vpn.-p -m -d -t -g")
    parser.add_argument('-p','--platform',
                        dest='platform',
                        default='auto',
                        nargs='?',
                        help="Target platforms, it can be openvpn, ovpn, mac, linux,"
                        "win, winp, android, all,auto. all by default.")
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
    elif args.platform.lower() == 'all':
        generate_ovpn(args.metric)
        generate_linux(args.metric)
        generate_mac(args.metric)
        generate_win(args.metric)
        #generate_winp(args.metric)
        generate_android(args.metric)
    elif args.platform.lower() == 'auto':
        #print sysstr
        generate_ovpn(args.metric)
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



















