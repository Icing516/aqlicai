#coding:utf-8

#判断线上环境公告是否及时更新
#期望设定脚本定时运行

import requests
import re
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import json
import smtplib
import time
from email.mime.text import MIMEText

now = int(time.time()) #->这是时间戳
timeArray = time.localtime(now)
nowDate = time.strftime("%Y-%m-%d", timeArray)
# print nowDate

url ='http://sso.aqlicai.cn/sso/login?returnUrl=http://www.aqlicai.cn/'
# agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
username ='wuhan123'
pubKey = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDZBOulvSxZBLlR8Fqp3svQe74O
    Gkcv8EqspTpWhWD9lOc0Yx6r+Bedvcv05Xpsy3CQZQbsnj1iI6xsvUzt02GxKCKa
    inm2/Z5xzT+VT3wD7+ziveEv0ZHYlKw/1pBb9O8qOlGfJVWR784RZ8JY4WcscWMj
    kVmj8rc4pWrI6nXGkwIDAQAB
    -----END PUBLIC KEY-----
    '''
login = 'http://sso.aqlicai.cn/user/login'
notice ='http://www.aqlicai.cn/notice/new-notice?'
search = 'http://www.aqlicai.cn/ajax/noticev2/search'

#获取加密后的密码
def get_pwd():
    rsakey = RSA.importKey(pubKey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(username))
    print cipher_text
    return cipher_text


#完成登录，并返回登录后重定向页面的session
def get_response():
    #获取首页的xsrf参数和session
    session1 = requests.session()
    page1 = session1.get(url)
    # 获取登录参数_xsrf
    reg1 = r'"_xsrf" value="(.*?)"'
    pattern1 = re.compile(reg1)
    math1 = re.findall(pattern1, page1.text)
    xsrf = math1[0]
    print 'xsrf=',xsrf

    #完成登录
    post_data1 = {
        '_xsrf': xsrf,
        'password': get_pwd(),
        'returnUrl': 'http://www.aqlicai.cn/',
        'username':'wuhan'
    }
    html1 = session1.post(login, post_data1)

    #获取登录页面返回的重定向链接的cookie
    urldata = json.loads(html1.content)
    print 'urldata=',urldata
    urljs = urldata['data']
    url2 = urljs['url']
    print 'url2=',url2

    session2 = requests.session()
    t2 = session2.get(url2)
    post_data2 = {
            # 'keyword':ciku1,
            'order_by':'title_score',
            'start_time': '1990-01-01',
            'end_time': nowDate,
            'limit': '20',
            'offset': '0'
        }
    html2 = session2.post(search,post_data2)
    result = html2.content
    print 'result=',result
    timeList = []
    resultdata = json.loads(result)
    print resultdata
    items = resultdata['data']['items']
    # print items
    return items

#获得返回的研报搜索结果
def check_notice():
    timeList = []
    items = get_response()
    for item in items:
        time1 = item['publish_at']
        # print time1
        timeArray = time.localtime(time1)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        if otherStyleTime ==nowDate:
            timeList.append(otherStyleTime)
        else:
            print "不是最新的公告"
    # print timeList
    sum = len(timeList)
    print "首页共有",sum,"篇今日公告"
    send_email(sum)

def send_email(sum):
    sender = 'xfang@niub.la'
    receiver = 'xfang@abcft.com'
    smtpserver = 'mail.niub.la'
    username = 'xfang@niub.la'
    password = 'fx152961627@dvt'
    subject = u'测试报告'
    mail_msg = """
    <p>研报列表页公告是最新的！</p>
    """
    msg = MIMEText(mail_msg ,'html', 'utf-8')  # mailboy：邮件正文；html：邮件格式
    msg['Subject'] = subject  # 邮件标题
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    check_notice()

