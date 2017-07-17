#coding:utf-8

#下载的数据是一整张表
import xlwt
import json
# filename = u'F:\\pycharm\\licai\\ciku.txt' # txt文件目录
workbook = xlwt.Workbook() #注意Workbook的开头W要大写
sheet2 = workbook.add_sheet('sheet2',cell_overwrite_ok=True)
filename ='F:\\pycharm\\licai\\test.json'
i=0
with open(filename,'r') as json_file:
    for line in json_file.readlines():
        # data =[]
        data =json.loads(line)
        text =data['legends']
        if text!=[]:
            print text
            sheet2.write(i,0,u'%s'%text)
            i+=1
    workbook.save('F:\\pycharm\\licai\\legends.xls')
print "legends获取完毕！"