import adata

# # k_type: k线类型：1.日；2.周；3.月 默认：1 日k
# res_df = adata.stock.market.get_market(stock_code='601198', k_type=1, start_date='2024-10-10')
# print(res_df)

# df = adata.stock.info.get_stock_shares(stock_code='601198')	
# print(df)

# df_concept = adata.stock.info.get_concept_ths(stock_code='601198')
# print(df_concept)

# today = adata.stock.market.get_market_min(stock_code='601198')
# print(today)

# five = adata.stock.market.get_market_five(stock_code='601198')
# print(five)

# index_min = adata.stock.market.get_market_index_min()
# print(index_min)

cur_capital_flow = adata.stock.market.get_capital_flow_min(stock_code='601198').tail(1)
print(cur_capital_flow)

# bar = adata.stock.market.get_market_bar(stock_code='300394')
# bar.to_csv('output.csv', index=False)
# print(bar)

# day_capital_flow = adata.stock.market.get_capital_flow(stock_code='601198', start_date='2024-10-09')
# day_capital_flow.to_csv('output.csv', index=False)
# print(day_capital_flow)

final_value = cur_capital_flow[['main_net_inflow', 'sm_net_inflow', 'mid_net_inflow', 'lg_net_inflow', 'max_net_inflow']].sum().sum()
print("Final Value:", final_value)

