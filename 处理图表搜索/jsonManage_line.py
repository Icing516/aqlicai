#coding:utf-8

#处理格式，下载的数据是单独一个字段
import xlwt
import json
# filename = u'F:\\pycharm\\licai\\ciku.txt' # txt文件目录
# workbook = xlwt.Workbook() #注意Workbook的开头W要大写
# sheet2 = workbook.add_sheet('sheet2',cell_overwrite_ok=True)
#legends.json  处理之前的legends数据
#legends2.json 处理之后的数据（去掉了legends为空的）
filename =u'D:\workspace\处理图表搜索\\legends.json'
# i=0
with open(filename,'r') as json_file:
    fileObject = open(u'D:\workspace\处理图表搜索\\legends2.json', 'w')
    for line in json_file.readlines():
        data =json.loads(line)
        text =data['legends']
        if text!=[]:
            print text
            jsonObject =json.dumps(text)
            fileObject.write(jsonObject+'\n')
            # sheet2.write(i,0,u'%s'%text)
            # i+=1
    fileObject.close()
    # workbook.save('F:\\pycharm\\licai\\legends.xls ')
print "legends获取完毕！"