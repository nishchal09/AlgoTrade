# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 17:56:28 2021

@author: ACER
"""

from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt
import numpy as np




end_date = dt.date.today().strftime('%Y-%m-%d')
beg_date = (dt.date.today() - dt.timedelta(1825)).strftime('%Y-%m-%d') 
ticker = "HCLTECH.NS"
#ticker = "HAPPSTMNDS.NS"

yahoo_finance = YahooFinancials(ticker)
json_obj = yahoo_finance.get_historical_price_data(beg_date,end_date, "daily")
ohlv = json_obj[ticker]['prices']
temp =pd.DataFrame(ohlv)[["formatted_date","adjclose", "open", "close", "high", "low", "volume"]]
temp.set_index("formatted_date", inplace = True)
temp.dropna(inplace = True)

def OBV(DF):
    df = DF.copy()
    df['daily_ret'] = df['adjclose'].pct_change()
    df['direction'] = np.where(df['daily_ret'] >= 0, 1, -1)
    df['direction'][0] = 0
    df['vol_adj'] = df['volume']*df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df['obv']

df = OBV(temp)
df[1000:].plot()