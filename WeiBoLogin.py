# -*- coding: utf-8 -*- 
# 
# 
"""
body={'_wv':'5',
                '__rnd':int(time.time()),#访问这一页面的时间，以秒表示的13位整数
                '_k':int(time.time()),#本次登录第一次访问此微薄的时间，16位整数
                '_t':0,
                'count':'50',#第二次和第二次访问时都是15，第一次访问时是50
                'end_id':weiboidlist[0],#最新的这一项微博的mid
                'max_id':weiboidlist[len(weiboidlist)-1],#已经访问到的，也就是lazyload上面的这一项最旧的微博的mid
                'page':str(i+1),#要访问的页码
                'pagebar':1,#第二次是0，第三次是1，第一次没有这项
                'pre_page':str(i+1),#第二次和第三次都是本页页码，第一次访问是上页页码
                'uid':'684211790'}#博主的uid}
"""
# 
# 
# 
# 
# 
# 
import re
import json
import urllib
import base64
import hashlib
import requests
import sys
import rsa
import binascii
import random
import time
import urllib2
from sgmllib import SGMLParser
from pyquery import PyQuery as pyq
from datetime import datetime
import matplotlib.pyplot as pl



#reload(sys)

#sys.setdefaultencoding('gbk')


WBCLIENT = 'ssologin.js(v.1.4.5)'
sha1 = lambda x: hashlib.sha1(x).hexdigest()



def wblogin(username, password):
    session = requests.Session()
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sina'
        'SSOController.preloginCallBack&su=%s&rsakt=mod&client=%s' %
        (base64.b64encode(username), WBCLIENT)
    )
    pre_login_str = re.match(r'[^{]+({.+?})', resp.content).group(1)
    #print pre_login_str
    pre_login_json = json.loads(pre_login_str)
    rsaPublickey = int(pre_login_json['pubkey'], 16)
    pcid= pre_login_json['pcid']
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(pre_login_json['servertime']) + '\t' + str(pre_login_json['nonce']) + '\n' + str(password)
    encodedPassWord = rsa.encrypt(message, key) #加密
    encodedPassWord = binascii.b2a_hex(encodedPassWord)
    encodedUserName = urllib.quote(username)
    encodedUserName = base64.encodestring(encodedUserName)[:-1]
    data = {
         'entry': 'weibo',
         'gateway': '1',
         'from': '',
         'savestate': '7',
         'userticket': '1',
         'pagerefer':'',
         'ssosimplelogin': '1',
         'vsnf': '1',
         'vsnval': '',
         'su': encodedUserName,
         'service': 'miniblog',
         'servertime': pre_login_json['servertime'],
         'nonce': pre_login_json['nonce'],
         'pwencode': 'rsa2',
         'sp': encodedPassWord,
         'encoding': 'UTF-8',
         'prelt': '115',
         'rsakv' : pre_login_json['rsakv'],
         'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
         'returntype': 'META'
     }
    resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
    )

    login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
                          resp.content).group(1)

    resp = session.get(login_url)

    login_str = re.findall(r'{.+}', resp.content)[0]

    #2070   验证码错误            
    #4049   请输入验证码
    login_info=json.loads(login_str)
    if login_info['result']==False and login_info['errno']=='4049':
        pincode_url=r'http://login.sina.com.cn/cgi/pin.php?r=0&s=0&p='+pcid
        req_img = urllib2.Request(pincode_url)
        res_img = urllib2.urlopen(req_img)
        f = open('xinlang_pincode.png', 'wb')
        f.write(res_img.read())
        f.close()
        code = raw_input('Enter pincode : ')
        data = {
         'entry': 'weibo',
         'gateway': '1',
         'from': '',
         'savestate': '7',
         'userticket': '1',
         'pagerefer':'',
         'pcid':pcid,
         'door':code,
         'ssosimplelogin': '1',
         'vsnf': '1',
         'vsnval': '',
         'su': encodedUserName,
         'service': 'miniblog',
         'servertime': pre_login_json['servertime'],
         'nonce': pre_login_json['nonce'],
         'pwencode': 'rsa2',
         'sp': encodedPassWord,
         'encoding': 'UTF-8',
         'prelt': '115',
         'rsakv' : pre_login_json['rsakv'],
         'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
         'returntype': 'META'
        }
        #entry=weibo&gateway=1&from=&savestate=7&useticket=1&pagerefer=http%3A%2F%2Fweibo.com%2Fa%2Fdownload&&vsnf=1&su=MTU4MjExNzkzMjU%3D&service=miniblog&servertime=1370307192&nonce=0Y4G0F&pwencode=rsa2&rsakv=1330428213&sp=165e0ebbf8b2e3b0e4c72f6476fc913e1d3a1a470396c04eef485ca47697bd2d07848b36ce9e45ccdba3d84cebb9839c98fafff38c8732fca7c4421cf327b525771d7fe7bdf65bd351dad076f22abca5a2531313692745b168f06f70faa993afe723f1d8d55d28dc3421f83351ef1e28e964059de89c90ad6e916ccad0366907&encoding=UTF-8&prelt=47&url=http%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent.sinaSSOController.feedBackUrlCallBack&returntype=META
        #entry=weibo&gateway=1&from=&savestate=7&useticket=1&pagerefer=http%3A%2F%2Fweibo.com%2Fa%2Fdownload&vsnf=1&su=MTU4MjExNzkzMjU%3D&service=miniblog&servertime=1370307258&nonce=BLJ3KR&pwencode=rsa2&rsakv=1330428213&sp=057ba53d1e67fd5cba180b9eaf07dd969c2fdd87cff7ab7d72e0e772461fce29a1dd80629c1d0c4acb74fce0399629f3771b65705c2864592b36014a51784607d558a3ac89321756b15875bc3463926f40dc5ae939b0ff65ff988d2781e0d3b4f7a8b6e49dbaa66f1e26362b097f0a3fdefdbe9276ed87d70b49f962e2083461&encoding=UTF-8&prelt=43&url=http%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent.sinaSSOController.feedBackUrlCallBack&returntype=META
        resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
        )
        login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
                          resp.content).group(1)
        resp = session.get(login_url)
        login_str = re.findall(r'{.+}', resp.content)[0]
        login_info=json.loads(login_str)

    while login_info['result']==False and login_info['errno']=='2070':
        print str(login_info['errno'])+':reason=>'+login_info['reason'].encode('gb2312')
        pincode_url=r'http://login.sina.com.cn/cgi/pin.php?r=0&s=0&p='+pcid
        req_img = urllib2.Request(pincode_url)
        res_img = urllib2.urlopen(req_img)
        f = open('xinlang_pincode.png', 'wb')
        f.write(res_img.read())
        f.close()
        code = raw_input('Enter pincode : ')
        data = {
         'entry': 'weibo',
         'gateway': '1',
         'from': '',
         'savestate': '7',
         'userticket': '1',
         'pagerefer':'',
         'pcid':pcid,
         'door':code,
         'ssosimplelogin': '1',
         'vsnf': '1',
         'vsnval': '',
         'su': encodedUserName,
         'service': 'miniblog',
         'servertime': pre_login_json['servertime'],
         'nonce': pre_login_json['nonce'],
         'pwencode': 'rsa2',
         'sp': encodedPassWord,
         'encoding': 'UTF-8',
         'prelt': '115',
         'rsakv' : pre_login_json['rsakv'],
         'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
         'returntype': 'META'
        }
        #entry=weibo&gateway=1&from=&savestate=7&useticket=1&pagerefer=http%3A%2F%2Fweibo.com%2Fa%2Fdownload&&vsnf=1&su=MTU4MjExNzkzMjU%3D&service=miniblog&servertime=1370307192&nonce=0Y4G0F&pwencode=rsa2&rsakv=1330428213&sp=165e0ebbf8b2e3b0e4c72f6476fc913e1d3a1a470396c04eef485ca47697bd2d07848b36ce9e45ccdba3d84cebb9839c98fafff38c8732fca7c4421cf327b525771d7fe7bdf65bd351dad076f22abca5a2531313692745b168f06f70faa993afe723f1d8d55d28dc3421f83351ef1e28e964059de89c90ad6e916ccad0366907&encoding=UTF-8&prelt=47&url=http%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent.sinaSSOController.feedBackUrlCallBack&returntype=META
        #entry=weibo&gateway=1&from=&savestate=7&useticket=1&pagerefer=http%3A%2F%2Fweibo.com%2Fa%2Fdownload&vsnf=1&su=MTU4MjExNzkzMjU%3D&service=miniblog&servertime=1370307258&nonce=BLJ3KR&pwencode=rsa2&rsakv=1330428213&sp=057ba53d1e67fd5cba180b9eaf07dd969c2fdd87cff7ab7d72e0e772461fce29a1dd80629c1d0c4acb74fce0399629f3771b65705c2864592b36014a51784607d558a3ac89321756b15875bc3463926f40dc5ae939b0ff65ff988d2781e0d3b4f7a8b6e49dbaa66f1e26362b097f0a3fdefdbe9276ed87d70b49f962e2083461&encoding=UTF-8&prelt=43&url=http%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent.sinaSSOController.feedBackUrlCallBack&returntype=META
        resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
        )
        login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
                          resp.content).group(1)
        resp = session.get(login_url)
        login_str = re.findall(r'{.+}', resp.content)[0]
        login_info=json.loads(login_str)
    return session, login_info


class WeiBoInstance(object):
    def __init__(self, username,password):
        self.username=username
        self.password=password
        self.haslogin=False

    def login(self):
        
        if self.haslogin==True:
            #print 'login successed!'
            #print 'username=>'+ self.userdisplayname
            return True
        print 'starting login......'
        self.session,login_info=wblogin(self.username,self.password)
        if login_info['result']==False:
            print 'login failed'
            print str(login_info['errno'])+':reason=>'+login_info['reason'].encode('gb2312')


            self.haslogin=False
            return False
        else:
            self.uid = login_info['userinfo']['uniqueid']
            self.userurl = "http://weibo.com/u/"+self.uid+login_info['userinfo']['userdomain']
            self.userdisplayname=login_info['userinfo']['displayname'].encode('gb2312')
            print 'login successed!'
            print 'username=>'+ self.userdisplayname
            self.haslogin=True
            return True
            #resp = session.get(url)
        pass

    def resuestpage(self,pageurl='',requesttimeout=None):
        if self.haslogin==False:
            print 'please login first'
            return None
        if pageurl=='':
            pageurl=self.userurl
        return self.session.get(pageurl,timeout=requesttimeout)
        pass
        

if __name__ == '__main__':
    zzhWeibo=WeiBoInstance('15821179325','2327651')
    if zzhWeibo.login()==False:
        sys.exit(0)


    sys.exit(0)
    datablog=zzhWeibo.resuestpage('http://weibo.com/u/1684211790?from=profile&wvr=5&loc=tagweibo').content
    #print datablog
    weibo_page_num_str=re.findall(r'<strong\snode-type=.{2}weibo.{2}>\d+',datablog)[0]
    weibo_page_num=int(weibo_page_num_str[weibo_page_num_str.rfind('>')+1:])
    targetNamestr=re.findall(r'<span class=.{2}name.{2}>.{1,30}<.{2}span>',datablog)[0]
    print targetNamestr
    targetNamestr=targetNamestr[targetNamestr.rfind('">')+2:targetNamestr.rfind('<')]
    print targetNamestr
    #print datablo
    #http://weibo.com/u/1684211790?from=profile&wvr=5&loc=tagweibo&page=4&pre_page=3&end_id=3583067878801192&end_msign=-1
    ss=str(int(time.time()))
    weibotime=re.findall(r'\d{4}-\d+-\d+\s\d+:\d+.{70}684211790',datablog)
    weiboid=re.findall(r'mid=\d{10,16}&name=',datablog)
    print len(weiboid)
    weiboidlist=[]
    for i in weiboid:
        weiboidlist.append(i[i.find('=')+1:i.find('&')])
    datalist=[]
    file = open('weibodata.txt', 'w')
    for i in weibotime:
        datalist.append(datetime.strptime(i[0:i.find('"')-1],'%Y-%m-%d %H:%M'))
        file.write(i[0:i.find('"')-1]+'\n')
    end_id=weiboidlist[0]
    print '============'+end_id
    body='http://weibo.com/aj/mblog/mbloglist?_wv=5&page=1&count=15&pre_page=1&_k='+ss+'&_t=0&max_id='+str(weiboidlist[len(weiboidlist)-1])+'&end_id='+end_id+'&pagebar=0&uid=1684211790&__rnd='+ss;
    datablog=zzhWeibo.resuestpage(body).content
        #print datablog
        #print datablog
    weibotime=re.findall(r'\d{4}-\d+-\d+\s\d+:\d+.{70}684211790',datablog)
    for j in weibotime:
        datalist.append(datetime.strptime(j[0:j.find('"')-1],'%Y-%m-%d %H:%M'))
        file.write(j[0:j.find('"')-1]+'\n')
    weiboid=re.findall(r'mid=\d{10,16}&name=',datablog)
    print len(weiboid)
    weiboidlist=[]
    for j in weiboid:
        weiboidlist.append(j[j.find('=')+1:j.find('&')])

    body='http://weibo.com/aj/mblog/mbloglist?_wv=5&page=1&count=15&pre_page=1&_k='+ss+'&_t=0&max_id='+str(weiboidlist[len(weiboidlist)-1])+'&end_id='+end_id+'&pagebar=1&uid=1684211790&__rnd='+ss;
    datablog=zzhWeibo.resuestpage(body).content
    weibotime=re.findall(r'\d{4}-\d+-\d+\s\d+:\d+.{70}684211790',datablog)
    for j in weibotime:
        datalist.append(datetime.strptime(j[0:j.find('"')-1],'%Y-%m-%d %H:%M'))
        file.write(j[0:j.find('"')-1]+'\n')
    weiboid=re.findall(r'mid=\d{10,16}&name=',datablog)
    weiboidlist=[]
    for j in weiboid:
        weiboidlist.append(j[j.find('=')+1:j.find('&')])

    print str(weiboidlist[0])

    weibo_page_num=int(weibo_page_num/45)+1
    print weibo_page_num
    for i in range(weibo_page_num):
        print 'first request analysis index==>'+str(i)
        body='http://weibo.com/u/1684211790?from=profile&wvr=5&loc=tagweibo&page='+str(i+2)+'&pre_page='+str(i+1)+'&end_id='+end_id+'&end_msign=-1'
        datablog=zzhWeibo.resuestpage(body).content
        weibotime=re.findall(r'\d{4}-\d+-\d+\s\d+:\d+.{70}684211790',datablog)
        for j in weibotime:
           datalist.append(datetime.strptime(j[0:j.find('"')-1],'%Y-%m-%d %H:%M'))
           file.write(j[0:j.find('"')-1]+'\n')
        weiboid=re.findall(r'mid=\d{10,16}&name=',datablog)
        weiboidlist=[]
        for j in weiboid:
            weiboidlist.append(j[j.find('=')+1:j.find('&')])
        ss=str(int(time.time()))
        print 'second request analysis index==>'+str(i)

        body='http://weibo.com/aj/mblog/mbloglist?_wv=5&__rnd='+ss+'&_k='+ss+'_t=0&count=15&end_id='+end_id+'&max_id='+str(weiboidlist[len(weiboidlist)-1])+'&page='+str(i+1)+ '&pagebar=0&pre_page='+str(i+1)+'&uid=1684211790'
        datablog=zzhWeibo.resuestpage(body).content

        #print datablog
        #print datablog
        weibotime=re.findall(r'\d{4}-\d+-\d+\s\d+:\d+.{70}684211790',datablog)
        for j in weibotime:
           datalist.append(datetime.strptime(j[0:j.find('"')-1],'%Y-%m-%d %H:%M'))
           file.write(j[0:j.find('"')-1]+'\n')
        weiboid=re.findall(r'mid=\d{10,16}&name=',datablog)
        #print weiboid
        weiboidlist=[]
        for j in weiboid:
            weiboidlist.append(j[j.find('=')+1:j.find('&')])
        print 'third request analysis index==>'+str(i)
        body='http://weibo.com/aj/mblog/mbloglist?_wv=5&__rnd='+str(int(time.time()))+'&_k='+str(int(time.time()))+'_t=0&count=15&end_id='+end_id+'&max_id='+weiboidlist[len(weiboidlist)-1]+'&page='+str(i+1)+ '&pagebar=1&pre_page='+str(i+1)+'&uid=1684211790'
        datablog=zzhWeibo.resuestpage(body).content
        weibotime=re.findall(r'\d{4}-\d+-\d+\s\d+:\d+.{70}684211790',datablog)
        for j in weibotime:
           datalist.append(datetime.strptime(j[0:j.find('"')-1],'%Y-%m-%d %H:%M'))
           file.write(j[0:j.find('"')-1]+'\n')
        weiboid=re.findall(r'mid=\d{10,16}&name=',datablog)
        weiboidlist=[]
        for i in weiboid:
            weiboidlist.append(i[i.find('=')+1:i.find('&')])
        #print len(weibotime)
        
    print 'get total num:'+str(len(datalist))
    file.close()
    



    #xd-e6a833f450b2205255ab7bf30df90e69587a