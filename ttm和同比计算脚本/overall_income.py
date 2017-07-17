from utils import *

RESULT_FILENAME='overall_income.csv';

'''
    Get overall_income from the latest year value
'''
def get_overall_income(current_time):
    least_overall_income=0;
    last_end_overall_income=0;
    last_overall_income=0;
    overall_income=0;
    # Get 2016-09-30 income
    db.query("SELECT account_date,overall_income FROM company_profit_sheet WHERE stock_code="+STOCK_CODE+" AND account_date<='"+string_current_time+"' ORDER BY account_date DESC limit 1");
    least_overall_incomeSet = db.store_result()
    if least_overall_incomeSet.num_rows() != 0:
        least_overall_income=least_overall_incomeSet.fetch_row(1,1);
        least_date=least_overall_income[0]['account_date'];
        string_last_date = last_year_to_string(least_overall_income);
        string_last_end_date = last_year_end_date_to_string(least_overall_income);
        least_overall_income = least_overall_income[0]['overall_income'];
        # Get 2015-09-30 income
        db.query(
            "SELECT account_date,overall_income FROM company_profit_sheet WHERE stock_code=" + STOCK_CODE + " AND account_date<='" + string_last_date + "' ORDER BY account_date DESC limit 1");
        last_overall_incomeSet = db.store_result()
        if last_overall_incomeSet.num_rows() != 0:
            last_overall_income = last_overall_incomeSet.fetch_row(1, 1);
            last_date = last_overall_income[0]['account_date'];
            last_overall_income = last_overall_income[0]['overall_income'];
        # Get 2015-12-31 income
        db.query("SELECT account_date,overall_income FROM company_profit_sheet WHERE stock_code=" + STOCK_CODE + " AND account_date<='" + string_last_end_date + "' ORDER BY account_date DESC limit 1");
        last_end_date_incomeSet = db.store_result();
        if last_end_date_incomeSet.num_rows() != 0:
                last_end_date_income = last_end_date_incomeSet.fetch_row(1, 1);
                last_end_date = last_end_date_income[0]['account_date'];
                last_end_overall_income = last_end_date_income[0]['overall_income'];
        overall_income=least_overall_income+last_end_overall_income-last_overall_income;
        return overall_income;

db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,overall_income" + '\n');
f.close();
while True:
    current_time = timeSet.fetch_row(1,1);
    if current_time==():
        break;
    else:
        j=j+1;
        #get current_time
        string_current_time = date_to_string(current_time);
        #get overall_income
        string_overall_income = get_overall_income(current_time);
        write_to_csv(string_current_time+","+str(string_overall_income),RESULT_FILENAME);
print "Total date count"+str(j);

