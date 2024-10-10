import adata
import pandas as pd

# Fetch all stock information
all_stock_info = adata.stock.info.all_code()

# Filter for Shanghai stocks
sh_stocks = all_stock_info[all_stock_info['exchange'] == 'SH']

# Select relevant columns
sh_stocks_df = sh_stocks[['stock_code', 'short_name']]

# Save to CSV
sh_stocks_df.to_csv('shanghai_stocks.csv', index=False)