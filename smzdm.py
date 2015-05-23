#!/usr/bin/python
# -*- coding:utf-8 -*-

smzdm_account   =   ''  #引号中添加自己的账号密码即可
smzdm_passwd    =   ''

email_address   =   ''  #自己的email地址, 我用的是QQ，如果是别的邮箱，请在后面修改smtp的地址。
email_passwd    =   ''

import cookielib
import urllib2
import urllib
import json

class smzdm:
    info        = {}

    def __init__(self, usr, psw):
        self.info["user_login"] =   usr
        self.info["user_pass"]  =   psw
        self.info["rememberme"] =   '1'

        #内建一个自动存cookie的opener
        self.cookie         = cookielib.LWPCookieJar()
        self.cookieHandler  = urllib2.HTTPCookieProcessor(self.cookie)
        opener              = urllib2.build_opener(self.cookieHandler)
        urllib2.install_opener(opener)


    #自动登录，并存cookie
    def login(self):

        userinfo    =   urllib.urlencode(self.info)
        url         =   "http://www.smzdm.com/user/login/jsonp_check"
        geturl      =   url + '?' + userinfo
        req         =   urllib2.Request(geturl)

        # add header
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36')
        req.add_header('Referer', 'http://www.smzdm.com/')  #防盗链

        response    = urllib2.urlopen(req)

    #签到
    def signIn(self):
        url = "http://www.smzdm.com/user/qiandao/jsonp_checkin"
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) \
        #AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36')

        response = urllib2.urlopen(req)

    # 获取签到信息，积分、登陆天数等等
    def getInfo(self):
        url = "http://www.smzdm.com/user/info/jsonp_get_current"
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_2) \
        #AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36')

        response = urllib2.urlopen(req)

        jsonInfo = response.read()  #读取json信息

        dic = json.loads(jsonInfo[1:-1])    #[1:-1]去掉htmlInfo里面的'('，然后转成字典
        if True == dic['user']['checkin']['has_checkin']:
            return True, dic['user']['point'], dic['user']['checkin']['daily_attendance_number']    #return login status, point, checkin days
        else:
            return False, '0', '0'


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

def email(username, password, status, days, points):
    msg = MIMEMultipart()

    #判断是否签到成功
    if status == True:
        txt = u"SMZDM，连续签到%s天，积分为%s分" % (days, points)
        msg['Subject'] = Header(txt)

    else:
        msg['Subject'] = Header("SMZDM签到——失败，请检查。", 'utf-8')

    msg['From'] = '什么值得买'
    msg['To']   = '签到'

    s = smtplib.SMTP_SSL()
    s.connect('smtp.qq.com', '465')     # 用的是QQ邮箱
    #s.set_debuglevel(1)
    s.login(username, password)
    s.sendmail(email_address, [email_address], msg.as_string())


if __name__ == '__main__':
    a = smzdm(smzdm_account, smzdm_passwd)
    a.login()
    a.signIn()
    #print u"签到成功"
    status, points, days = a.getInfo()

    email(email_address, email_passwd, status, days, points)
