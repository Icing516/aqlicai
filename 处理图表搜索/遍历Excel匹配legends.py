#coding:utf-8

import xlwt,xlrd
import json
from xlutils import copy

#用关联词库的每一行的每一个词去匹配legends字段中的text
#且将不同的line，BAR，UNKNOWN，CURVE，COLUMNAR，AREA分别统计
#关联词库存放的位置
filename1 =u'D:\\workspace\\处理图表搜索\\guanlianciku.xls'
filename2 =u'D:\\workspace\\处理图表搜索\\guanlianciku2.xls'
legefile =u'D:\\workspace\\处理图表搜索\\legends1.json'
#先读取Excel文件
workbook =xlrd.open_workbook(filename1,'r')
sheet = workbook.sheet_by_name('sheet1')
rows =sheet.nrows
cols =sheet.ncols

#row:行数
#col:列数
#获取每一行的列数据去legefile文件中遍历查询
for row in range(0,rows):
    line =sheet.row_values(row)
    for col in range(0,cols-1,2):
        LINE = 0
        CURVE = 0
        UNKNOWN = 0
        BAR = 0
        COLUMNAR = 0
        AREA = 0

        lineValue = line[col]
        print line[col]

        #读legends2.json里面的每一行，用line[col]去匹配
        with open(legefile,'r') as legend_file:
            for lines in legend_file.readlines():
                data = json.loads(lines)
                for i in range(0, len(data)):
                    # print data[i]['text']
                    # print data[i].keys()
                    text =data[i]['text']
                    #如果data[i]['text']的值为空则跳过
                    if text is None:
                        pass
                    #判断搜索词在数据库的legends字段是否存在，存在则判断图表的样式，如:LINE+1
                    if lineValue==text:
                        if 'line' in data[i].keys():
                            LINE +=1
                        elif 'curve' in data[i].keys():
                            CURVE +=1
                        elif 'bar' in data[i].keys():
                            BAR +=1
                        elif 'unknown' in data[i].keys():
                            UNKNOWN +=1
                        elif 'columnar' in data[i].keys():
                            COLUMNAR +=1
                        elif 'area' in data[i].keys():
                            AREA +=1

        dict = {
                'LINE': LINE,
                'CURVE': CURVE,
                'UNKNOWN': UNKNOWN,
                'BAR': BAR,
                'COLUMNAR': COLUMNAR,
                'AREA': AREA
                }
        book = xlrd.open_workbook(filename2)
        new_book = copy.copy(book)
        sheet2 =new_book.get_sheet(0)
        sheet2.write(row,col+1,u'%s'%dict)
        new_book.save(filename2)
legend_file.close()
