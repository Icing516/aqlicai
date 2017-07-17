#coding:utf-8

import requests
import re
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import json
import xlrd,xlwt
from xlutils import copy

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
search = 'http://www.aqlicai.cn/ajax/reportv2/search'
filename = u'D:\workspace\公司近义词库.xls'

#获取加密后的密码
def get_pwd():
    rsakey = RSA.importKey(pubKey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(username))
    # print  cipher_text
    return cipher_text

#读取词库，作为查询参数
def get_ciku():
    ciku_list = []
    data =xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colValues = table.col_values(0)
    # for i in xrange(0, nrows):
    #     rowValues = table.row_values(i,0)  # 某一行数据
    for item in colValues:
            # print item
        ciku_list.append(item)
    # print case_list[2]
    return ciku_list

#完成登录，并返回登录后重定向页面的session
def get_response():
    # ciku =[]
    #获取首页的xsrf参数和session
    session1 = requests.session()
    page1 = session1.get(url)
    # 获取登录参数_xsrf
    reg1 = r'"_xsrf" value="(.*?)"'
    pattern1 = re.compile(reg1)
    math1 = re.findall(pattern1, page1.text)
    xsrf = math1[0]

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
    urljs = urldata['data']
    url2 = urljs['url']
    # print 'url2 =',url2

    session2 = requests.session()
    t2 = session2.get(url2)
    ciku =get_ciku()
    # print ciku
    # len =len(ciku)
    resultList = []
    for ciku1 in ciku:
        print "ciku=",ciku1
        post_data2 = {
            'keyword':ciku1,
            'start_time': '1990-01-01',
            'end_time': '2017-06-14',
            'limit': '20',
            'offset': '0'
            }
        html2 = session2.post(search,post_data2)
        result = html2.content
        # print result

        resultList.append(get_result(result))
    return resultList

#获得返回的研报搜索结果
def get_result(result):
    resultlist =[]
    resultdata = json.loads(result)
    code = resultdata['code']
    reports = resultdata['data']
    if code ==0:
        if 'items' in reports:
            resultlist.append(u'搜索正常')
            # print True
        else:
            resultlist.append(u'搜索无结果')
            # print False
        print "搜索结果=",resultlist[0]
    elif code ==-1:
        resultlist.append(u'error')
    return resultlist

#将搜索结果写入到Excel文件中
def writeResult(resultList):
    book = xlrd.open_workbook(filename)
    new_book = copy.copy(book)
    sheet = new_book.get_sheet(0)
    # rows = sheet.nrows
    # sheet.write(i, 2, u'%s'%resultlist)
    i = 0
    for result in resultList:
        sheet.write(i, 1, u'%s'%result[0])
        i = i + 1
    new_book.save(filename)

if __name__ == '__main__':
    # get_ciku()
    writeResult(get_response())


