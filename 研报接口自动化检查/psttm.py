#coding:utf-8
# from __future__ import division
import MySQLdb

conn= MySQLdb.connect(
        host='10.11.255.110',
        port = 31306,
        user='rreportor',
        passwd='saWQR432QR',
        db ='r_reportor',
        )


cur = conn.cursor()
# cur.execute("insert into student values('2','Tom','3 year 2 class','9')")

stock_price=cur.execute("SELECT close_price FROM company_share_price WHERE stock_code='000788' ORDER BY TIME DESC LIMIT 0,1")
info = cur.fetchmany(stock_price)
stock_price = info[0][0]
print "stock_price =",stock_price

income=cur.execute("SELECT overall_income FROM company_profit_sheet WHERE stock_code='000788' ORDER BY account_date DESC limit 0,5")
info = cur.fetchmany(income)
sum_profit = info[0][0]+info[3][0]-info[4][0]
print "sum_profit =",sum_profit

sum_stock=cur.execute("SELECT stock_total FROM company_stock_structure WHERE stock_code ='000788.SZ' AND change_date<=(SELECT NOW()) ORDER BY change_date DESC LIMIT 0,1")
info = cur.fetchmany(sum_stock)
sum_stock =info[0][0]
print "sum_stock=",sum_stock

value = stock_price*sum_stock
print "value =",value

ttm = value/sum_profit
print 'ttm =',ttm


cur.close()
conn.commit()
conn.close()