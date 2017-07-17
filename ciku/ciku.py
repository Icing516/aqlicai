# -*- coding:utf-8 -*-

import xlwt

f = open(u'D:\workspace\ciku\【For Dev】关键财务指标近义词库-20170510.txt','r')
List =[]
while True:
    line =f.readline().decode('utf-8')
    print line
    if line:
        p1 =line.split(' ')
        # print p1[0]
        List.append(p1[0])
        pass
    else:
        break
f.close()

book = xlwt.Workbook()
sheet = book.add_sheet('sheet1')
i=0
for list in List:
    print list
    sheet.write(i,0,list) #第0行第一列写入内容
    i +=1
book.save(u'D:\workspace\ciku\财务指标近义词库.xls')