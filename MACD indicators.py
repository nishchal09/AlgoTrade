# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 00:41:57 2021

@author: ACER
"""

from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt

all_ticker = ["HAPPSTMNDS.NS" ]


close_price = pd.DataFrame()

end_date = dt.date.today().strftime('%Y-%m-%d')
beg_date = (dt.date.today() - dt.timedelta(1825)).strftime('%Y-%m-%d') 
ticker = "HCLTECH.NS"

yahoo_finance = YahooFinancials(all_ticker[0])
json_obj = yahoo_finance.get_historical_price_data(beg_date,end_date, "daily")
ohlv = json_obj[all_ticker[0]]['prices']
temp =pd.DataFrame(ohlv)[["formatted_date","adjclose"]]
temp.set_index("formatted_date", inplace = True)
temp.dropna(inplace = True)
close_price["adjclose"] = temp["adjclose"]
close_price.dropna(inplace = True)

#1) moving_average_indicator

def MACD(DF, a,b,c):
    
    df = DF.copy()
    
    df["MA_fast"] = df["adjclose"].ewm(span = a, min_periods= a).mean()
    df["MA_slow"] = df["adjclose"].ewm(span = b, min_periods= b).mean()
    df["MACD"] = df["MA_fast"] - df["MA_slow"]
    df["Signal"] = df["MACD"].ewm(span = c, min_periods= c).mean()
    df.dropna(inplace = True)
    return df

df = MACD(close_price, 12, 26 ,9)


