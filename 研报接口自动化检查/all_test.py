#coding=utf-8

import unittest
#这里需要导入测试文件
import test,baidu,youdao,tuyoumi
import HTMLTestRunner
import time,os,datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#定义发送邮件函数
def sentmail(file_new):
    mail_from ="fangxin@szzbmy.com"
#    mail_to ="fangxin67@139.com"
    mail_to ="fangxin516@163.com"
#    mail_to ="981524415@qq.com"
    #定义正文
    f =open(file_new,'rb')
    mail_body =f.read()
    f.close()
    msg =MIMEText(mail_body,_subtype='html',_charset ='utf-8')
    msg['Subject'] =u"Icing的测试报告"  #定义标题
    #定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date'] =time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp =smtplib.SMTP()
    smtp.connect('smtp.ym.163.com')
    smtp.login("fangxin@szzbmy.com", "fx152961627")
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()
    print "email has send out!"

#查找测试报告目录，找到最新生成的测试报告文件
def sendreport():
    result_dir ="D:\\MyWorkpace\\tuyoumi\\src\\result"
    lists =os.listdir(result_dir)
    lists.sort(key =lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not os.path.isdir(result_dir+"\\"+fn) else 0)
    print (u"最新测试生成的报告："+lists[-1])
    #找到最新政策的文件 os.path.join()拼接文件名称
    file_new =os.path.join(result_dir,lists[-1])
    print file_new
    #调用发邮件模块
    sentmail(file_new)

testunit=unittest.TestSuite()

#将测试用例加入到测试容器(套件)中
testunit.addTest(unittest.makeSuite(baidu.Baidu))
testunit.addTest(unittest.makeSuite(youdao.Youdao))
testunit.addTest(unittest.makeSuite(test.Mytest))
testunit.addTest(unittest.makeSuite(tuyoumi.CreateGame))

#获取当前时间
now =time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
#定义个报告存放路径，支持相对路径。
filename = "D:\\MyWorkpace\\tuyoumi\\src\\result\\"+now+"result.html"
fp = file(filename, 'wb')

runner =HTMLTestRunner.HTMLTestRunner(
                                      stream=fp,
                                      title=u'百度搜索测试报告',
                                      description=u'用例执行情况：')

if __name__ =="__main__":
    now =time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
    #执行测试用例
    runner.run(testunit)
    fp.close()
    sendreport()

