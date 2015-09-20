#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################
# name:updateHosts
# author:https://github.com/ladder1984
# version:1.3.3
# license:MIT
############################

test=0
ip_check_url = 'http://www.google.com.hk/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
protocol = "http"
proxy_detected = False


import urllib2
import platform
import datetime
import time
import re
import os
import shutil
import ConfigParser
import sys
import socket

import subprocess

import argparse
socket.setdefaulttimeout(10.0)
from threading import Timer
def handler(fh):
    fh.close()
#fh = urlopen(url)
#t = Timer(8.0, handler,[fh])
#t.start()
#data = fh.read()    #如果二进制文件需要换成二进制的读取方式
#t.cancel()




# default setting
hosts_folder = ""
hosts_location = hosts_folder + "hosts"

source_list = ['https://raw.githubusercontent.com/vokins/simpleu/master/hosts']
not_block_sites = 0
always_on = 0
# default setting

#errorLog = open('errorLog.txt', 'a')

# Check proxy
def check_proxy(protocol, pip):
    global proxy_detected
    try:
        proxy_handler = urllib2.ProxyHandler({protocol:pip})
        opener = urllib2.build_opener(proxy_handler)
        #opener.addheaders = [('User-agent', user_agent)]
        #这句加上以后无法正常检测，不知道是什么原因。
        urllib2.install_opener(opener)
        req = urllib2.Request(ip_check_url)
        time_start = time.time()
        conn = urllib2.urlopen(req)
        #conn = urllib2.urlopen(ip_check_url)
        time_end = time.time()
        detected_pip = conn.read()
        proxy_detected = True
    except urllib2.HTTPError, e:
        print "ERROR: Code ", e.code
        return False
    except Exception, detail:
        print "ERROR: ", detail
        return False
    return proxy_detected


def get_cur_info():
    return(sys._getframe().f_back.f_code.co_name)


def exit_this():
    #errorLog.close()
    sys.exit()


def check_connection():
    sleep_seconds = 1200
    i = 0
    for i in range(sleep_seconds):
        try:
            socket.gethostbyname("www.baidu.com")
            break
        except socket.gaierror:
            time.sleep(1)
    if i == sleep_seconds - 1:
        exit_this()


def check_system():
    global hosts_folder
    global hosts_location
    if platform.system() == 'Windows':
        hosts_folder = os.environ['SYSTEMROOT']+"\\System32\\drivers\\etc\\"
    elif platform.system() == 'Linux'or platform.system() == 'Darwin':
        hosts_folder = "/etc/"
    else:
        exit_this()
    hosts_location = hosts_folder + "hosts"


def get_config():
    global source_list
    global not_block_sites
    global always_on,test
    if os.path.exists('config.ini'):
        try:
            # 清除Windows记事本自动添加的BOM
            content = open('config.ini').read()
            content = re.sub(r"\xfe\xff", "", content)
            content = re.sub(r"\xff\xfe", "", content)
            content = re.sub(r"\xef\xbb\xbf", "", content)
            open('config.ini', 'w').write(content)

            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            source_id = config.get('source_select', 'source_id')
            source_list = source_id.split(",")

            for i in range(len(source_list)):
                source_list[i]=config.get('source_select', 'source'+source_list[i])

            not_block_sites = config.get("function", "not_block_sites")
            always_on = config.get("function","always_on")
        except BaseException, e:
            if test==1:print str(e)
            #errorLog.write(str(datetime.datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')
            exit_this()


def backup_hosts():
    global test
    try:
        if (not os.path.isfile(hosts_folder + 'backup_hosts_original_by_updateHosts')) and \
                os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder+'hosts', hosts_folder+'backup_hosts_original_by_updateHosts')
        if os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder+'hosts', hosts_folder+'backup_hosts_last_by_updateHosts')
    except BaseException, e:
        if test==1:print str(e)
        #errorLog.write(str(datetime.datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')
        exit_this()


def download_hosts():
    if not os.path.exists('hosts.txt'):
        for x in source_list:
            dh(x)
        if os.path.exists('hosts_from_web_tmp'):os.remove('hosts_from_web_tmp')        


def dh(x):
    global test,protocol,user_agent,ip_check_url,proxy_detected
    proxy_detected = False
    try:
        #x=re.sub("#invalid","",x)
        if os.path.exists('hosts_from_web_tmp'):os.remove('hosts_from_web_tmp')
        if platform.system() == 'Windows' and os.path.exists('wget.exe'):
            #print(1)
            os.system("wget --no-check-certificate -c " + re.sub("#invalid","",x) + " -O hosts_from_web_tmp")            
        elif platform.system() == 'Linux':
            #print(2)
            os.system("wget " + re.sub("#invalid","",x) + " -O hosts_from_web_tmp")
        else:
            #print(3)
            data=urllib2.urlopen(re.sub("#invalid","",x), data=None, timeout=8)
            open("hosts_from_web_tmp","w").write(data.read()+'\n')
            data.close()
    except BaseException, e:
        if test==1:print str(e)
        #errorLog.write(str(datetime.datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')
        exit_this()
    finally:        
        if os.path.exists('hosts_from_web_tmp'):
            #print any(open("hosts_from_web_tmp").read().strip())
            if any(open("hosts_from_web_tmp").read().strip()):
                current_proxy = "103.7.200.79:80"
                hostsline=open("hosts_from_web_tmp").readlines()
                for line in hostsline:
                    #print line.split(" ")[0]
                    if line.find("www.google.com")>0:
                        #print line.split(" ")[0]
                        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
                        for ip in reip.findall(line):
                            #print "ip>>>", ip
                            current_proxy=ip
                proxy_detected = check_proxy(protocol, current_proxy)
                if proxy_detected:
                #    print (" WORKING: " + current_proxy)
                    open("hosts_from_web","a").write(open("hosts_from_web_tmp").read()+'\n')
                #else:
                #    print " FAILED: %s " % ( current_proxy, )
        if proxy_detected:
            #print 33333333
            if x.find("#invalid")>0:
                #print 44444444444
                #x=re.sub("#invalid","",x)
                data=open("config.ini").read()
                data=re.sub(x,re.sub("#invalid","",x),data)
                #print data
                open("config.ini","w").write(data)
        else:
            #print 5555555555555
            #x=re.sub("#invalid","",x)
            data=open("config.ini").read()
            data=re.sub(re.sub("#invalid","",x) + "#invalid",re.sub("#invalid","",x),data)
            data=re.sub(re.sub("#invalid","",x),re.sub("#invalid","",x) + "#invalid",data)
            #print data
            open("config.ini","w").write(data)            
        if test==1:print x

def process_hosts():
    if os.path.exists('hosts.txt') or os.path.exists('hosts_from_web'):
        if os.path.exists('hosts.txt') or any(open("hosts_from_web").read().strip()):
            hosts_content = open('hosts', 'w')
            if not os.path.exists('hosts.txt'):
                file_from_web = open('hosts_from_web')
            else:
                file_from_web = open('hosts.txt')
            hosts_from_web = file_from_web.read()
            file_user_defined = open('hosts_user_defined.txt')
            hosts_user_defined = file_user_defined.read()
            hosts_content.write('#hosts_user_defined\n')
            hosts_content.write(hosts_user_defined)
            hosts_content.write('\n#hosts_user_defined\n')
            hosts_content.write('\n\n#hosts_by_hostsUpdate\n\n')
            if not_block_sites is "1":
                hosts_from_web = re.sub("127.0.0.1", "#not_block_sites", hosts_from_web)
            hosts_content.write(hosts_from_web)
            hosts_content.write('\n#hosts_by_hostsUpdate')
            hosts_content.close()
            file_from_web.close()
            file_user_defined.close()
   


def move_hosts():
    try:
        if os.path.exists('hosts'):shutil.move("hosts", hosts_location)
        if os.path.exists('hosts_from_web'):os.remove('hosts_from_web')
        if os.path.exists('hosts_from_web_tmp'):os.remove('hosts_from_web_tmp')
    except BaseException, e:
        if test==1:print str(e)
        #errorLog.write(str(datetime.datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')
        exit_this()


def fortest():
    print " Test mode on."




def main():
    global test
    if test==1:fortest()
    #check_connection()
    check_system()
    get_config()
    backup_hosts()
    download_hosts()
    process_hosts()
    move_hosts()
    #errorLog.close()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="update hosts. -t")
    parser.add_argument('-t','--test',
                        dest='test',
                        default=0,
                        nargs='?',
                        type=int,
                        help="start test mode,echo errs.")   
    args = parser.parse_args()
    if args.test!=0:test=args.test
    main()

if always_on == "1":
    while 1:
        time.sleep(3600)
        main()