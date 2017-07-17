from utils import *

RESULT_FILENAME='stock_total.csv';

'''
    Get stock_total
'''
def get_stock_code(current_time):
    db.query(
        "SELECT stock_total FROM company_stock_structure WHERE stock_code = "+STOCK_CODE+" and change_date <= '"+string_current_time+"' ORDER BY change_date DESC limit 1");
    stock_totalSet = db.store_result()
    if stock_totalSet.num_rows() != 0:
        stock_total=stock_totalSet.fetch_row(1,1);
        return stock_total[0]['stock_total'];



db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,stock_total" + '\n');
f.close();
while True:
    current_time = timeSet.fetch_row(1,1);
    if current_time==():
        break;
    else:
        j=j+1;
        #get current_time
        string_current_time = date_to_string(current_time);
        #get stock_code
        string_stock_code = get_stock_code(current_time);
        write_to_csv(string_current_time+","+str(string_stock_code),RESULT_FILENAME);
print "Total date count"+str(j);

