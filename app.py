from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import concurrent.futures
from datetime import datetime
import adata
import os

app = Flask(__name__)

def get_final_value(stock_code):
    cur_capital_flow = adata.stock.market.get_capital_flow_min(stock_code=stock_code).tail(1)
    return cur_capital_flow[['main_net_inflow', 'sm_net_inflow', 'mid_net_inflow', 'lg_net_inflow', 'max_net_inflow']].sum().sum() / 10000

def fetch_latest_data():
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
    top_30_stocks_df = results_df.sort_values(by='final_value', ascending=False).head(30)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return top_30_stocks_df, current_time

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        top_30_stocks_df, current_time = fetch_latest_data()
        stocks = top_30_stocks_df.to_dict(orient='records')
        return render_template('index.html', stocks=stocks, current_time=current_time)
    return render_template('index.html', stocks=None, current_time=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))