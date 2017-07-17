from utils import *

RESULT_FILENAME='free_float_stock.csv';

'''
    Get free_float_stock
'''
def get_stock_code(current_time):
    db.query(
        "SELECT free_float_stock FROM company_stock_structure WHERE stock_code = "+STOCK_CODE+" and change_date <= '"+string_current_time+"' ORDER BY change_date DESC limit 1");
    free_float_stockSet = db.store_result()
    if free_float_stockSet.num_rows() != 0:
        free_float_stock=free_float_stockSet.fetch_row(1,1);
        return free_float_stock[0]['free_float_stock'];



db.query("SELECT TIME FROM company_share_price WHERE stock_code="+STOCK_CODE+" ORDER BY TIME DESC");
timeSet = db.store_result();
j=0;
# Write table header
f = open(RESULT_FILENAME, 'w');
f.write("Time,free_float_stock" + '\n');
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

