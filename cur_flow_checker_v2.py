import adata
import pandas as pd
import concurrent.futures
from datetime import datetime

def get_final_value(stock_code):
    cur_capital_flow = adata.stock.market.get_capital_flow_min(stock_code=stock_code).tail(1)
    return cur_capital_flow[['main_net_inflow', 'sm_net_inflow', 'mid_net_inflow', 'lg_net_inflow', 'max_net_inflow']].sum().sum() / 10000

def main():
    sh_stocks_df = pd.read_csv('shanghai_stocks.csv', dtype={'stock_code': str})
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_final_value, row['stock_code']): row for _, row in sh_stocks_df.iterrows()}
        for future in concurrent.futures.as_completed(futures):
            row = futures[future]
            try:
                results.append((row['stock_code'], row['short_name'], future.result()))
            except Exception as e:
                print(f"Error processing stock {row['stock_code']}: {e}")

    results_df = pd.DataFrame(results, columns=['stock_code', 'short_name', 'final_value'])

    top_20_stocks_df = results_df.sort_values(by='final_value', ascending=False).head(20)

    for _, row in top_20_stocks_df.iterrows():
        print(f"股票代码：{row['stock_code']} 股票名称：{row['short_name']} 当前净流入: {round(row['final_value'], 2)} 万元")

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"当前时间: {current_time}")

    return top_20_stocks_df, current_time

if __name__ == '__main__':
    top_20_stocks_df, finish_time = main()