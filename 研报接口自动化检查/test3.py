#-*- coding:utf-8 -*-

import requests
import time
import lxml
from lxml import etree
# import email_config
import cookielib

agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
headers = {
    "Host": "jira.niub.la",
    'Referer':'https://jira.niub.la/login.jsp',
    'User-Agent': agent
}

post_url = 'https://jira.niub.la/rest/gadget/1.0/login'
# post_url = 'https://jira.niub.la/login.jsp'
postdata = {
    'atl_token': '',
    'login': '登录',
    'os_cookie': 'true',
    'os_destination': '',
    'os_password': 'fx152961627@dvt',
    'os_username': 'xfang',
    # 'os_captcha': ''
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')

login_page = session.post(post_url, data=postdata, headers=headers)
print login_page.text
tree = etree.HTML(login_page.text)
print "tree1=",tree.xpath("//span[@class='aui-avatar-inner']/img/@alt")[0]
print "tree=",tree
