from utils import *

RESULT_FILENAME='parent_equity.csv';

'''
    Get parent_equity from the latest year value
'''
def get_parent_equity(current_time):
    db.query(
        "select parent_equity from company_balance_sheet WHERE stock_code="+STOCK_CODE+" and account_date<='"+string_current_time+"' ORDER BY account_date DESC limit 1");
    parent_equitySet = db.store_result()
    if parent_equitySet.num_rows() != 0:
        parent_equity=parent_equitySet.fetch_row(1,1);
        return parent_equity[0]['parent_equity'];

db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,parent_equity" + '\n');
f.close();
while True:
    current_time = timeSet.fetch_row(1,1);
    if current_time==():
        break;
    else:
        j=j+1;
        #get current_time
        string_current_time = date_to_string(current_time);
        #get parent_equity
        string_parent_equity = get_parent_equity(current_time);
        write_to_csv(string_current_time+","+str(string_parent_equity),RESULT_FILENAME);
print "Total date count"+str(j);

