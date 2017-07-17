#coding:utf-8

#判断线上环境公告是否及时更新
#期望设定脚本定时运行

import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

# now = int(time.time()) #->这是时间戳
# timeArray = time.localtime(now)
# nowDate = time.strftime("%Y-%m-%d", timeArray)
# print nowDate

# mail_host="smtp.139.com"  #设置服务器
# # mail_host ="mail.abcft.com"
# mail_user="15986671443@139.com"#用户名
# mail_pass ='fx152961627'
# # mail_pass="189240"   #口令
# sender ='15986671443@139.com'
# receivers =['fangxin516@163.com']
#
# message = MIMEText('Python 公告报告...', 'plain', 'utf-8')
# message['From'] = Header("Icing")
# message['To'] =  Header("Icing666")
#
# subject = '公告测试报告'
# message['Subject'] = Header(subject, 'utf-8')
#
#
# try:
#     smtpObj = smtplib.SMTP()
#     smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
#     smtpObj.ehlo()
#     smtpObj.starttls()
#     smtpObj.ehlo()
#     smtpObj.login(mail_user,mail_pass)
#     time.sleep(2)
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print "邮件发送成功"
#     smtpObj.quit()
# except smtplib.SMTPException as e:
#     print e
#     print "Error: 无法发送邮件"
#     smtpObj.quit()

# def get_sum():
#     sum =2
#     return sum
#
def send_email():
    sender = 'xfang@niub.la'
    receiver ='xfang@abcft.com'
    smtpserver ='mail.niub.la'
    username = 'xfang@niub.la'
    password ='fx152961627@dvt'
    subject=u'测试报告'
    mail_msg =  """
    <p>研报列表页公告是最新的！</p>
    """
    msg=MIMEText(mail_msg,'html','utf-8')   #mailboy：邮件正文；html：邮件格式
    msg['Subject']=subject   #邮件标题
    msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp=smtplib.SMTP()
    smtp.connect(smtpserver,587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
#
if __name__ == '__main__':
    send_email()

# import time
# import sched
#
# schedule = sched.scheduler ( time.time, time.sleep )
#
# def func(string1,float1):
#     print "now is",time.time()," | output=",string1,float1
#
# print time.time()
# schedule.enter(2,0,func,("test1",time.time()))
# schedule.enter(2,0,func,("test1",time.time()))
# schedule.enter(3,0,func,("test1",time.time()))
# schedule.enter(4,0,func,("test1",time.time()))
# schedule.run()
# print time.time()

#
# #! /usr/bin/env python
# #coding=utf-8
# import time, os, sched
#
# # 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# # 第二个参数以某种人为的方式衡量时间
# schedule = sched.scheduler(time.time, time.sleep)
#
# def perform_command(cmd, inc):
#     # 安排inc秒后再次运行自己，即周期运行
#     schedule.enter(inc, 0, perform_command, (cmd, inc))
#     os.system(cmd)
#
# def timming_exe(cmd, inc = 60):
#     # enter用来安排某事件的发生时间，从现在起第n秒开始启动
#     schedule.enter(inc, 0, perform_command, (cmd, inc))
#     # 持续运行，直到计划时间队列变成空为止
#     schedule.run()
#
# print("show time after 3 seconds:")
# timming_exe("echo %time%", 3)