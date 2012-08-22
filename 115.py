#!/usr/bin/env python
#-*- coding:utf-8 -*-
accounts_here = [
    {"account":'115115115','password':'000000'},
    {"account":'116116116','password':'000000'},
]

import urllib
import urllib2
import cookielib
import json
import re,time,os
class Log:
  def __init__(self):
    self.PATH=os.path.abspath(os.path.expanduser('.'))
    self.fd=open(self.PATH+"/log.txt",'a')
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    self.log("## %s"%t,False)
  def log(self,s,indent=True):
    if indent:
      s="  %s"%s
    print(s.decode("u8"))
    self.fd.write(s)
    self.fd.write("\n")

class Here115:
  def __init__(self):
    cj = cookielib.CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(self.opener)
    self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686)')]

  def login(self, username, password):
    url = 'https://passport.115.com/?ac=login'
    data = urllib.urlencode({'login[account]':username, 'login[passwd]':password,'login[time]':'on'})
    req = urllib2.Request(url, data)
    try:
      fd = self.opener.open(req)
    except Exception, e:
      l.log('网络连接错误！')
      return False
    res=fd.read()
    fd.close()
    if re.search('location\.href="http://115.com"', res) == None:
      l.log('%s 密码不正确！' % username)
      return False
    else:
      l.log('%s 登陆成功，准备摇奖...' % username),
      return True

  def pick_space(self):
    url = 'http://115.com/?ct=file&ac=userfile&aid=1&cid=0&tpl=list_pg&limit=30'
    req = urllib2.Request(url)
    fd = self.opener.open(req)
    token_page = fd.read()
    fd.close()
    token = re.search("take_token:\s'(\w+)'", token_page)
    if not token:
      l.log('今天已经摇过了...')
      return

    url = 'http://115.com/?ct=ajax_user&ac=pick_space&token=' + token.group(1)
    req = urllib2.Request(url)
    fd = self.opener.open(req)
    res_json = json.loads(fd.read())
    fd.close()
    if res_json['state'] == False:
      l.log('摇奖失败！')
      return
    str=u'> 获取空间：%s, 总空间：%s, 已使用：%s, 获取雨露：%d' % (res_json['picked'], res_json['total_size'], res_json['used_percent'], res_json['exp'])
    l.log(str.encode("u8"))


if __name__ == '__main__':
  l=Log()
  for i in accounts_here:
    h = Here115()
    if not h.login(i['account'],i['password']):
      continue
    h.pick_space()

