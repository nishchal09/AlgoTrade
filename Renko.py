# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 13:10:53 2021

@author: ACER
"""

from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt
from stocktrends import Renko



close_price = pd.DataFrame()

end_date = dt.date.today().strftime('%Y-%m-%d')
beg_date = (dt.date.today() - dt.timedelta(1825)).strftime('%Y-%m-%d') 
ticker = "HCLTECH.NS"
#ticker = "HAPPSTMNDS.NS"

yahoo_finance = YahooFinancials(ticker)
json_obj = yahoo_finance.get_historical_price_data(beg_date,end_date, "daily")
ohlv = json_obj[ticker]['prices']
temp =pd.DataFrame(ohlv)[["formatted_date","adjclose", "open", "close", "high", "low"]]
temp.set_index("formatted_date", inplace = True)
temp.dropna(inplace = True)
close_price["adjclose"] = temp["adjclose"]
close_price.dropna(inplace = True)

#1) TR(True Range) and ATR (Avg True Range)

def ATR(DF, n):
        
    df = DF.copy()
    df["H-L"] = abs(df["high"] - df["low"])
    df["H-PC"] = abs(df["high"] - df["adjclose"].shift(1))
    df["L-PC"] = abs(df["low"] - df["adjclose"].shift(1))
    df["TR"] = df[["H-L", "H-PC" , "L-PC"]].max(axis = 1, skipna = False)
    df["ATR"] = df["TR"].rolling(n).mean()
    df2 = df.drop(["H-L", "H-PC", "L-PC"], axis = 1)
    df2.dropna(inplace = True)
    return df2

DF = temp
def Renko_DF(DF):
    df = DF.copy()
    df.reset_index(inplace = True)
    df = df.iloc[:,[0,1,2,4,5]]
    df.columns = ["date", "close" , "open", "high", "low"]
    Renko_df = Renko(df)
    
    Renko_df.brick_size = round(ATR(DF,120)['ATR'][-1],0)
    df2 = Renko_df.get_ohlc_data()
    
    return df2

