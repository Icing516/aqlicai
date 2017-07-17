#coding:utf-8

import requests
import re
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import json


url ='http://sso.aqlicai.cn/sso/login?returnUrl=http://www.aqlicai.cn/'

#获取cookie并使用
S1= requests.session()
t1=S1.get(url)
# print t1.text

#获取登录参数_xsrf
reg1 = r'"_xsrf" value="(.*?)"'
pattern1 =re.compile(reg1)
math1 =re.findall(pattern1,t1.text)
xsrf = math1[0]
# print "_xsrf =",xsrf

#获取登录参数pubKey
reg2 = r'"pubKey" value="(.*?)"'
pattern2 =re.compile(reg2)
math2 =re.findall(pattern2,t1.text)
pubKey = math2[0]
# print "页面抓取的pubkey =\n",pubKey

reg3 = r'lOc0Yx6r(.*?)ziveEv0'
pattern3 =re.compile(reg3)
math3 =re.findall(pattern3,pubKey)
pubKey1 =math3[0]
# print "pubKey1 =",pubKey1

pwd ='----BEGIN PUBLIC KEY-----\n'+pubKey+'\n-----END PUBLIC KEY-----'
# print 'pwd =',pwd

pubKey2 ='''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDZBOulvSxZBLlR8Fqp3svQe74O
Gkcv8EqspTpWhWD9lOc0Yx6r+Bedvcv05Xpsy3CQZQbsnj1iI6xsvUzt02GxKCKa
inm2/Z5xzT+VT3wD7+ziveEv0ZHYlKw/1pBb9O8qOlGfJVWR784RZ8JY4WcscWMj
kVmj8rc4pWrI6nXGkwIDAQAB
-----END PUBLIC KEY-----
'''

message ='wuhan123'
# print pubKey2
rsakey =RSA.importKey(pubKey2)
cipher = Cipher_pkcs1_v1_5.new(rsakey)
cipher_text = base64.b64encode(cipher.encrypt(message))
# print cipher_text

agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
headers1 = {
    "Host": "sso.aqlicai.cn",
    'Referer':'http://sso.aqlicai.cn/sso/login?returnUrl=http://www.aqlicai.cn/',
    'User-Agent': agent
}

login ='http://sso.aqlicai.cn/user/login'
post_data1 ={
    '_xsrf':xsrf,
    'password':cipher_text,
    'returnUrl':'http%3A%2F%2Fwww.aqlicai.cn%2F',
    'username':'wuhan'
}
html1 = S1.post(login,post_data1,headers1)
# print html1.content

#获取重定向页面的cookie
urldata=json.loads(html1.content)
urljs=urldata['data']
url2 =urljs['url']
# print 'url2 =',url2

S2 = requests.session()
t2 = S2.get(url2)
# print t2.content
# print S2.cookies

headers2 = {
    "Host": "www.aqlicai.cn",
    'Referer':'http://www.aqlicai.cn/report-search',
    'User-Agent': agent
}

post_data2 = {
    'keyword':'平安银行',
    'start_time': '1990-01-01',
    'end_time': '2017-06-14',
    'limit': '20',
    'offset': '0'
}

sraech = 'http://www.aqlicai.cn/ajax/reportv2/search'
html2 = S2.post(sraech,post_data2,headers2)
print 'html2 =',html2.content
