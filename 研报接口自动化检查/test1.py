#coding:utf-8

import MySQLdb
import xlwt

'''
将company_profit_sheet表里面的最近四个季度的营业收入列出来，判断最新的是（12、09、06、03）
中的哪一个，用if语句分别执行不同的算法
'''

# stock = 000788
conn= MySQLdb.connect(
        host='10.11.255.110',
        port = 31306,
        user='rreportor',
        passwd='saWQR432QR',
        db ='r_reportor',
        )
cur = conn.cursor()
date_list =[]
stock_list =[]
price_list =[]
profit_list =[]
ttm_list =[]


book = xlwt.Workbook()  # 创建工作簿
sheet = book.add_sheet('ttm', cell_overwrite_ok=True)
sheet.col(0).width = 5000
sheet.col(2).width = 3000
sheet.col(3).width = 3000
sheet.col(4).width = 4000
#写入第一列字段名
row0 = ['date','stock_price','stock_sum','profit','ttm']
for i in range(0,len(row0)):
    sheet.write(0,i,row0[i])
#先处理日期,找到每天收盘对应的日期
s2=cur.execute("SELECT TIME FROM company_share_price WHERE stock_code= '000788' ORDER BY TIME DESC")
info = cur.fetchmany(s2)
# print info
# t1 = info[0]
# print repr(t1)
i =0
for t in info:
        t1 = t[0]
        t2 ='"%s"' % t1
        #将所有的日期写入列表中date_list
        date_list.append(t2)
        print t2
        #按照收盘价日期找到最近的总股本
        sq1 ="SELECT stock_total FROM company_stock_structure WHERE stock_code = '000788.SZ' AND change_date <=" +str(t2)+" ORDER BY change_date DESC limit 0,1"
        s1 = cur.execute(sq1)
        inf1 = cur.fetchmany(s1)
        stock_sum = inf1[0][0]
        print "stock_sum =",stock_sum
        #将所有的总股本写入列表stock_list
        stock_list.append(stock_sum)

        #按照收盘日期找到收盘价
        sq2 = "SELECT close_price FROM company_share_price WHERE stock_code='000788' AND TIME <=" +str(t2)+ " ORDER BY TIME DESC"
        # print sq2
        s2 = cur.execute(sq2)
        inf2 = cur.fetchmany(s2)
        stock_price = inf2[0][0]
        print "stock_price=",stock_price
        #将每天的收盘价写入列表price_list
        price_list.append(stock_price)

        # 查询出前5条营业收入
        sq3 = "SELECT account_date,overall_income FROM company_profit_sheet WHERE stock_code='000788' and account_date <=" +str(t2)+" ORDER BY account_date DESC LIMIT 0,5"
        s3 = cur.execute(sq3)
        info = cur.fetchmany(s3)
        p0 = info[0][1]
        p1 = info[1][1]
        p2 = info[2][1]
        p3 = info[3][1]
        p4 = info[4][1]
        print "p4 =",p4
        m1 = info[0][0].month
        # print "m1 =", m1

        if p4 != None:
                if m1 == 12:
                        profit = p0
                elif m1 == 9:
                        profit = p0 + p3 - p4
                elif m1 == 6:
                        profit = p0 + p2 - p4
                elif m1 == 3:
                        profit = p0 + p1 - p4
                else:
                        print "数据错误"
                print "profit =",profit
        else:
                print "数据错误！"
                profit = "error"
                exit()
        #将每次的营业收入写入列表profit_list
        profit_list.append(profit)

        # 计算TTM
        ttm = (stock_sum * stock_price) / profit
        # print "ttm=", ttm
        #将每次计算的ttm写入到列表ttm_list
        ttm_list.append(ttm)

        # 将查询的结果写入到Excel文件中
        sheet.write(i+1, 0, date_list[i])
        sheet.write(i+1, 1, price_list[i])
        sheet.write(i+1, 2, stock_list[i])
        sheet.write(i+1, 3, profit_list[i])
        sheet.write(i+1, 4, ttm_list[i])
        book.save(r'D:\ttm\ttm.xls')
        i += 1

cur.close()
conn.commit()
conn.close()