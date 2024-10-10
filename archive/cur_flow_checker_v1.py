import adata
import concurrent.futures
import time

def get_final_value(stock_code):
    # Get the capital flow for the current stock
    cur_capital_flow = adata.stock.market.get_capital_flow_min(stock_code=stock_code).tail(1)
    final_value = cur_capital_flow[['main_net_inflow', 'sm_net_inflow', 'mid_net_inflow', 'lg_net_inflow', 'max_net_inflow']].sum().sum()
    return final_value / 10000

# Start timing
start_time = time.time()

all_stock_info = adata.stock.info.all_code()
sh_stocks = all_stock_info[all_stock_info['exchange'] == 'SH']
sh_stocks_df = sh_stocks[['stock_code', 'short_name']]

results = []

# Use ThreadPoolExecutor to parallelize the fetching of capital flow data
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_stock = {executor.submit(get_final_value, row['stock_code']): row for index, row in sh_stocks_df.iterrows()}
    for future in concurrent.futures.as_completed(future_to_stock):
        row = future_to_stock[future]
        stock_code = row['stock_code']
        short_name = row['short_name']
        try:
            final_value_in_wan = future.result()
            results.append((stock_code, short_name, final_value_in_wan))
        except Exception as e:
            print(f"Error processing stock {stock_code}: {e}")

# Sort the results by final value in descending order and select the top 20
top_20_stocks = sorted(results, key=lambda x: x[2], reverse=True)[:20]

# Print the top 20 stocks
for stock_code, short_name, final_value_in_wan in top_20_stocks:
    print("股票代码：", stock_code, "股票名称：", short_name, "当前净流入:", round(final_value_in_wan, 2), "万元")

# End timing
end_time = time.time()

# Print the total processing time
print(f"处理时间: {end_time - start_time:.2f} seconds")