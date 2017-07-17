from utils import *

RESULT_FILENAME='parent_netprofit.csv';

'''
    Get parent_netprofit from the latest year value
'''
def get_parent_netprofit(current_time):
    least_parent_netprofit=0;
    last_end_parent_netprofit=0;
    last_parent_netprofit=0;
    parent_netprofit=0;
    # Get 2016-09-30 netprofit
    db.query("SELECT account_date,parent_netprofit FROM company_profit_sheet WHERE stock_code="+STOCK_CODE+" AND account_date<='"+string_current_time+"' ORDER BY account_date DESC limit 1");
    least_parent_netprofitSet = db.store_result()
    if least_parent_netprofitSet.num_rows() != 0:
        least_parent_netprofit=least_parent_netprofitSet.fetch_row(1,1);
        least_date=least_parent_netprofit[0]['account_date'];
        string_last_date = last_year_to_string(least_parent_netprofit);
        string_last_end_date = last_year_end_date_to_string(least_parent_netprofit);
        least_parent_netprofit = least_parent_netprofit[0]['parent_netprofit'];
        # Get 2015-09-30 netprofit
        db.query(
            "SELECT account_date,parent_netprofit FROM company_profit_sheet WHERE stock_code=" + STOCK_CODE + " AND account_date='" + string_last_date + "' ORDER BY account_date DESC limit 1");
        last_parent_netprofitSet = db.store_result()
        if last_parent_netprofitSet.num_rows() != 0:
            last_parent_netprofit = last_parent_netprofitSet.fetch_row(1, 1);
            last_date = last_parent_netprofit[0]['account_date'];
            last_parent_netprofit = last_parent_netprofit[0]['parent_netprofit'];
        # Get 2015-12-31 netprofit
        db.query("SELECT account_date,parent_netprofit FROM company_profit_sheet WHERE stock_code=" + STOCK_CODE + " AND account_date='" + string_last_end_date + "' ORDER BY account_date DESC limit 1");
        last_end_date_incomeSet = db.store_result();
        if last_end_date_incomeSet.num_rows() != 0:
            last_end_date_income = last_end_date_incomeSet.fetch_row(1, 1);
            last_end_date = last_end_date_income[0]['account_date'];
            last_end_parent_netprofit = last_end_date_income[0]['parent_netprofit'];
        if last_end_parent_netprofit==0:
            parent_netprofit="Null";
        if last_parent_netprofit==0:
            parent_netprofit = "Null";
        else:
            parent_netprofit=least_parent_netprofit+last_end_parent_netprofit-last_parent_netprofit;
        return parent_netprofit;

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
        string_parent_netprofit = get_parent_netprofit(current_time);
        write_to_csv(string_current_time+","+str(string_parent_netprofit),RESULT_FILENAME);
print "Total date count"+str(j);

