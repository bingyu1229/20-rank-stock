import adata
import time  # Import the time module

# Record the start time
start_time = time.time()

all_stock_info = adata.stock.info.all_code()
sh_stocks = all_stock_info[all_stock_info['exchange'] == 'SH']
sh_stocks_df = sh_stocks[['stock_code', 'short_name']]

results = []

for index, row in sh_stocks_df.iterrows():
    stock_code = row['stock_code']
    short_name = row['short_name']
    
    # Get the capital flow for the current stock
    cur_capital_flow = adata.stock.market.get_capital_flow_min(stock_code=stock_code).tail(1)
    final_value = cur_capital_flow[['main_net_inflow', 'sm_net_inflow', 'mid_net_inflow', 'lg_net_inflow', 'max_net_inflow']].sum().sum()
    final_value_in_wan = final_value / 10000
    
    # Append the result to the list
    results.append((stock_code, short_name, final_value_in_wan))

# Sort the results by final value in descending order and select the top 20
top_20_stocks = sorted(results, key=lambda x: x[2], reverse=True)[:20]

# Print the top 20 stocks
for stock_code, short_name, final_value_in_wan in top_20_stocks:
    print("股票代码：", stock_code, "股票名称：", short_name, "当前净流入:", round(final_value_in_wan, 2), "万元")

# Record the end time
end_time = time.time()

# Calculate and print the processing time
processing_time = end_time - start_time
print("Processing time:", processing_time, "seconds")