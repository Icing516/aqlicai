from utils import *
RESULT_FILENAME='bussiness_cash_netvalue.csv';

'''
    Get bussiness_cash_netvalue from the latest year value
'''
def get_bussiness_cash_netvalue(current_time):
    print string_current_time;
    db.query(
        "select bussiness_cash_netvalue from company_cash_sheet WHERE stock_code="+STOCK_CODE+" and account_date like '%12-31%' and account_date<='"+string_current_time+"' ORDER BY account_date DESC limit 1");
    bussiness_cash_netvalueSet = db.store_result()
    if bussiness_cash_netvalueSet.num_rows() != 0:
        bussiness_cash_netvalue=bussiness_cash_netvalueSet.fetch_row(1,1);
        print bussiness_cash_netvalue;
        return bussiness_cash_netvalue[0]['bussiness_cash_netvalue'];

db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,bussiness_cash_netvalue" + '\n');
f.close();
while True:
    current_time = timeSet.fetch_row(1,1);
    if current_time==():
        break;
    else:
        j=j+1;
        #get current_time
        string_current_time = date_to_string(current_time);
        #get bussiness_cash_netvalue
        string_bussiness_cash_netvalue = get_bussiness_cash_netvalue(current_time);
        write_to_csv(string_current_time+","+str(string_bussiness_cash_netvalue),RESULT_FILENAME);
print "Total date count"+str(j);

