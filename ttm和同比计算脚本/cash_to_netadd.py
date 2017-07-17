from utils import *

RESULT_FILENAME='cash_to_netadd.csv';

'''
    Get cash_to_netadd from the latest year value
'''
def get_cash_to_netadd(current_time):
    db.query(
        "select cash_to_netadd from company_cash_sheet WHERE stock_code="+STOCK_CODE+" and account_date like '%12-31%' and account_date<='"+string_current_time+"' ORDER BY account_date DESC limit 1");
    cash_to_netaddSet = db.store_result()
    if cash_to_netaddSet.num_rows() != 0:
        cash_to_netadd=cash_to_netaddSet.fetch_row(1,1);
        return cash_to_netadd[0]['cash_to_netadd'];



db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,cash_to_netadd" + '\n');
f.close();
while True:
    current_time = timeSet.fetch_row(1,1);
    if current_time==():
        break;
    else:
        j=j+1;
        #get current_time
        string_current_time = date_to_string(current_time);
        #get cash_to_netadd
        string_cash_to_netadd = get_cash_to_netadd(current_time);
        write_to_csv(string_current_time+","+str(string_cash_to_netadd),RESULT_FILENAME);
print "Total date count"+str(j);

