# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 18:51:06 2021

@author: ACER
"""

import yfinance as yf
import datetime as dt
import pandas as pd
import requests

print(dt.datetime.today())

stocks = ["PFC.NS", "BPCL.NS", "SBILIFE.NS","SUNPHARMA.NS","CADILAHC.NS"]
start = dt.datetime.today() - dt.timedelta(360)
end = dt.datetime.today()

ohlcv = {}

#period is used for 1,3,6 month and
# interval is used for 2month data (commonly for intraday)

cl_price = pd.DataFrame()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]
    
for ticker in stocks:
    ohlcv[ticker] = yf.download(ticker, start, end)
    
#IMPORT DATA FROM YAHOOFINANCIALS

from yahoofinancials import YahooFinancials

all_ticker = ["HCLTECH.NS", "WIPRO.NS","BSOFT.NS","HAPPSTMNDS.NS","INFY.NS", "TTML.NS" ]


close_price = pd.DataFrame()

end_date = dt.date.today().strftime('%Y-%m-%d')
beg_date = (dt.date.today() - dt.timedelta(1825)).strftime('%Y-%m-%d') 
ticker = "HCLTECH.NS"
for ticker in all_ticker:
     yahoo_finance = YahooFinancials(ticker)
     json_obj = yahoo_finance.get_historical_price_data(beg_date,end_date, "daily")
     ohlv = json_obj[ticker]['prices']
     temp =pd.DataFrame(ohlv)[["formatted_date","adjclose"]]
     temp.set_index("formatted_date", inplace = True)
     temp.dropna(inplace = True)
     close_price[ticker] = temp["adjclose"]
 
    
#IMPORT DATA FROM ALPHA VANTAGE

from alpha_vantage.timeseries import TimeSeries
import time

key_path = "DR3LMM8WRHVNP1Q8"
ticker = "CANBK"
ts = TimeSeries(key = key_path, output_format ='pandas') 
data = ts.get_intraday(symbol = ticker,outputsize = "full")[0]
data.columns = ["open","high", "low","close","volume"]

data = data.iloc[::-1]

new_tickers = ["SBIN.BO", "BPCL.BO" , "RBLBANK.BO", "HDFC.BO" ,"PFC.BO", "CANBK.BO"]

clo_price = pd.DataFrame()
api_call_count  = 0
start_time = time.time()

for tickers in new_tickers:
    ts = TimeSeries(key = key_path, output_format ='pandas')
    data = ts.get_intraday(symbol = tickers,interval = '1m',outputsize = 'compact')[0]
    api_call_count += 1
    data.columns = ["open","high", "low","close","volume"]
    data = data.iloc[::-1]
    clo_price[tickers] = data["close"]
    if api_call_count == 5:
        api_call_count = 0
        time.sleep(60 - ((time.time() - start_time)%60.0))
    
