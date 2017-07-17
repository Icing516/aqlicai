#coding:utf-8

import xlrd
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

filename = u'D:\workspace\处理图表搜索\\ciku.txt' # txt文件目录
workbook = xlwt.Workbook() #注意Workbook的开头W要大写
sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
# filename =u'F:\\pycharm\\licai\\关联词库'
j =0
with open(filename,'r+') as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
            break
        else:
            print lines
            linelist =lines.split('\t')
            print "linelist =", linelist
            i = 0
            for list in linelist:
                sheet1.write(j,i,u'%s'%list)
                i+=2
        j += 1
    workbook.save(u'D:\workspace\处理图表搜索\\guanlianciku.xls ')
file_to_read.close()
print u"文件读取完成！"
