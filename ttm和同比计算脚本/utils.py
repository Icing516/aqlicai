import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
import MySQLdb

STOCK_CODE="000788";

MYSQL_HOST='10.11.255.110'
MYSQL_PORT=31306
MYSQL_USER='rreportor'
MYSQL_PASSWORD='saWQR432QR'
MYSQL_DB='r_reportor'
db = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB, charset='utf8')

'''
    Change date from datetime.datetime To String
'''
def date_to_string(current_time):
    datetime = current_time[0]['TIME'];
    tt=datetime.timetuple();
    num=0;
    string_time='';
    for it in tt:
        if num<3:
            if num!=0:
                string_time=string_time+"-"+str(it);
            else:
                string_time = string_time+str(it);
            num=num+1;
        else:
            break;
    return string_time;

'''
    Get last year current time
'''
def last_year_to_string(current_time):
    datetime = current_time[0]['account_date'];
    tt=datetime.timetuple();
    num=0;
    string_time='';
    for it in tt:
        if num<3:
            if num!=0:
                string_time=string_time+"-"+str(it);
            else:
                it = it - 1;
                string_time = string_time+str(it);
            num=num+1;
        else:
            break;
    return string_time;


'''
    Get last year 12-31
'''
def last_year_end_date_to_string(current_time):
    datetime = current_time[0]['account_date'];
    tt=datetime.timetuple();
    num=0;
    string_time='';
    for it in tt:
        if num<3:
            if num==0:
                it = it - 1;
                string_time=string_time+str(it)+"-12-31";
            num=num+1;
        else:
            break;
    return string_time;

'''
    Write value to csv file
'''
def write_to_csv(string,filename):
    f = open(filename, 'a');
    f.write(string + '\n');
    f.close();
