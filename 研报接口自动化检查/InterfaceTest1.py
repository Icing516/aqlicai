#coding=utf-8

import requests, xlrd, time, sys
#导入需要用到的模块  xlrd，读取Excel的扩展工具
from xlutils import copy
#从xlutils模块中导入copy这个函数
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication 

dicparam={}  #字典
case_list = []  #列表，存储测试用例
responses = []
expectresults = []
res_code=[]
name = u'%s_测试结果.xls'%time.strftime('%Y-%m-%d-%H-%M-%S')
def readExcel(file_path):
    try:
        book = xlrd.open_workbook(file_path) #打开excel
    except Exception,e:
        #如果路径不在或者excel不正确，返回报错信息
        print '路径不在或者excel不正确',e
        return e
    else:
        sheet = book.sheet_by_index(0)#取第一个sheet页
        rows= sheet.nrows#取这个sheet页的所有行数
        #保存每一条case
        for i in range(rows):
            if i !=0:
                #把每一条测试用例添加到case_list中
                case_list.append(sheet.row_values(i))
                print i
        #调用接口测试的函数，把存所有case的list和excel的路径传进去，因为后面还需要把返回报文和测试结果写到excel中，

        
def urlparam(param):
    return param.replace(":","&")

#这个方法用来将传参转换为字典，用于post传参
def dicpost(p):
    if ',' in p:
        p1=p.split(',')
        for q1 in p1:
            k,v=q1.split(':')
            dicparam[k]=v
    else:
        for q in p:
            k,v=p.split(':')
            dicparam[k]=v
        
    return dicparam

def inter(case_list,file_path):
 
    for case in case_list:
        '''
        先遍历excel中每一条case的值，然后根据对应的索引取到case中每个字段的值
        '''
#        print case
        expectresult =case[3]
#        print "expectresult ="+expectresult
        expectresults.append(expectresult)

        try:
            method = case[2]   #请求方式
            url = case[0]    #请求url
            param = case[1]   #请求参数
#            expectresults =case[3]  #获得预期结果
            
        except Exception,e:
            return '测试用例格式不正确！%s'%e
        
        if method.upper() == 'GET':
            if param== '':
                new_url = url
            else:
                new_url = url+'?'+urlparam(param)
 
            results = requests.get(new_url).text
            code=requests.get(new_url).status_code
#            print results
#            print code
            responses.append(results)
            res_code.append(code)

        else:
            results = requests.post(url,data=dicpost(param)).text
#            print results
            code=requests.post(url,data=dicpost(param)).status_code
            responses.append(results)
            res_code.append(code)

def copy_excel(file_path,expectresults,responses,res_code,name):
   
    book = xlrd.open_workbook(file_path)
    new_book = copy.copy(book)
    sheet = new_book.get_sheet(0)
    i = 1
    j = 1
    k = 1
    for code in res_code:
        sheet.write(i,4,u'%s' %code)
        i=i+1
        
    for response in responses:
#        for expectresult in expectresults:
        sheet.write(j,5,u'%s'%response)
        j+=1
    print responses
    print expectresults
    for h in range(0,len(responses)):
        if responses[h] == expectresults[h]:
            sheet.write(k,6,'pass')
        else:
            sheet.write(k,6,'fail')
        k +=1
    
    
    new_book.save(name)

def sendEmail(name):
    sender='fangxin@szzbmy.com'
    receiver='fangxin67@139.com'
    subject=u'测试报告4'
    smtpserver='smtp.ym.163.com'
    username='fangxin@szzbmy.com'
    password='fx152961627'

    msg = MIMEMultipart() 
    msg["Subject"] = u"接口测试报告"
    msg["From"]  = sender 
    msg["To"]   = receiver 

    part = MIMEText("python test report,icing") 
    msg.attach(part) 

    part = MIMEApplication(open(name,'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=name) 
    msg.attach(part) 

    #msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp=smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print "测试结果邮件发送成功"

def InterfaceTest(file):
    readExcel(file)
    inter(case_list,file)
    copy_excel(file,expectresults,responses,res_code,name)
    sendEmail(name)
