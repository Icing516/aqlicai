from utils import *
from decimal import *
RESULT_FILENAME='yoy.csv';
stock_code="000001";

def date_to_string(current_time):
    datetime = current_time[0]['account_date'];
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


db.query("SELECT account_date FROM `company_finance_indicators` WHERE stock_code="+stock_code+" ORDER BY account_date DESC;");
timeSet = db.store_result();
while True:
    time = timeSet.fetch_row(1,1);
    if time == ():
        break;
    else:
        string_current_time = date_to_string(time);
        string_last_date = last_year_to_string(time);
        db.query("SELECT * FROM `company_finance_indicators` WHERE stock_code="+stock_code+" ORDER BY account_date DESC;");
        keysSet = db.store_result();
        current_field = keysSet.fetch_row(1,1)[0];
        current_field.pop('account_date');
        current_field.pop('ID');
        current_field.pop('report_period');
        current_field.pop('stock_code');
        keys=current_field.keys();
        for key in keys:
            db.query(
       "SELECT (SELECT " + key + " FROM company_finance_indicators WHERE stock_code = "+stock_code+" AND account_date = '"+string_last_date+"') AS a, (SELECT " + key + " FROM company_finance_indicators WHERE stock_code = "+stock_code+" AND account_date = '"+string_current_time+"') AS b, (SELECT (b-a)/ABS(a));");
            indicatorsSet = db.store_result();
            indicatorsValue = indicatorsSet.fetch_row(1, 1)[0]['(SELECT (b-a)/ABS(a))'];
            db.query(
       "SELECT "+key+" FROM `company_finance_indicators_yoy` WHERE stock_code = "+stock_code+" AND account_date = '"+string_current_time+"'");
            yoyIndicatorsSet = db.store_result();
            yoyIndicatorsValue = yoyIndicatorsSet.fetch_row(1, 1)[0][key];
            if isinstance(indicatorsValue, Decimal):
                indicatorsValue=round(indicatorsValue, 4);
            print string_current_time,key,indicatorsValue,yoyIndicatorsValue;

