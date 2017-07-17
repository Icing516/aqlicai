from utils import *
RESULT_FILENAME='least_parent_netprofit.csv';

'''
    Get parent_netprofit from the latest year value
'''
def get_least_parent_netprofit(current_time):
    print string_current_time;
    db.query(
        "select parent_netprofit from company_profit_sheet WHERE stock_code="+STOCK_CODE+" and account_date like '%12-31%' and account_date<='"+string_current_time+"' ORDER BY account_date DESC limit 1");
    least_parent_netprofitSet = db.store_result()
    if least_parent_netprofitSet.num_rows() != 0:
        least_parent_netprofit=least_parent_netprofitSet.fetch_row(1,1);
        return least_parent_netprofit[0]['parent_netprofit'];

db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,parent_netprofit" + '\n');
f.close();
while True:
    current_time = timeSet.fetch_row(1,1);
    if current_time==():
        break;
    else:
        j=j+1;
        #get current_time
        string_current_time = date_to_string(current_time);
        #get parent_netprofit
        string_least_parent_netprofit = get_least_parent_netprofit(current_time);
        write_to_csv(string_current_time+","+str(string_least_parent_netprofit),RESULT_FILENAME);
print "Total date count"+str(j);

