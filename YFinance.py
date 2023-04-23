#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ta
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy.stats import linregress


class Stock:
    
    def __init__(self):
        self.name = ''


    def stock(self):
        
        #today's date
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        
        # Calculate the start date as one year ago from today
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        
        
        #data = yf.download(self.name, start=start_date, end=end_date)
        
        # Download data for TCS for the last year
        #data = yf.download('TCS.NS', start=start_date, end=end_date)
    
        # caluculating EMA's
        
        # data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
        # data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        # data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
        # data['EMA100'] = data['Close'].ewm(span=100, adjust=False).mean()
        # data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()
        
        # # Compute the 20 day average volume
        # data['VolumeAvg20'] = data['Volume'].rolling(window=20).mean()
        
        
        # data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
        
        # macd = ta.trend.MACD(data['Close'], window_fast=12, window_slow=26, window_sign=9)
        # data['MACD'] = macd.macd()
        # data['MACD_signal'] = macd.macd_signal()
        # data['MACD Above Signal'] = data['MACD'] > data['MACD_signal']
        
        
        
        

        def calculate_technical_indicators(name, start_date, end_date, ema_span=9, ema_span_list=[20, 50, 100, 200], rsi_window=14, macd_fast=12, macd_slow=26, macd_signal=9):
            data = yf.download(name, start=start_date, end=end_date)
            data['EMA{}'.format(ema_span)] = data['Close'].ewm(span=ema_span, adjust=False).mean()
            for span in ema_span_list:
                data['EMA{}'.format(span)] = data['Close'].ewm(span=span, adjust=False).mean()
            data['VolumeAvg20'] = data['Volume'].rolling(window=20).mean()
            data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=rsi_window).rsi()
            macd = ta.trend.MACD(data['Close'], window_fast=macd_fast, window_slow=macd_slow, window_sign=macd_signal)
            data['MACD'] = macd.macd()
            data['MACD_signal'] = macd.macd_signal()
            data['MACD Above Signal'] = data['MACD'] > data['MACD_signal']
            return data
        data = calculate_technical_indicators(self.name, start_date, end_date)
        df = pd.DataFrame(data)
        
    
 
    # Define a function to calculate the slope and y-intercept of a trendline
        def calculate_trendline(x, y):
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            return slope * x + intercept
    
    # Define the time periods for each trendline
        short_term_period = 10
        mid_term_period = 50
        long_term_period = 100
        
        # Calculate the short-term trendline using linear regression
        short_term_trendline = calculate_trendline(np.arange(len(df['Close']))[-short_term_period:], df['Close'][-short_term_period:])
        
        # Calculate the mid-term trendline using linear regression
        mid_term_trendline = calculate_trendline(np.arange(len(df['Close']))[-mid_term_period:], df['Close'][-mid_term_period:])
        
        # Calculate the long-term trendline using linear regression
        long_term_trendline = calculate_trendline(np.arange(len(df['Close']))[-long_term_period:], df['Close'][-long_term_period:])
        
        # Plot the price data and trendlines
        fig, ax = plt.subplots(figsize=(10, 6))
        
        df['Close'].plot(ax=ax, label='Close')
        ax.plot(df.index[-short_term_period:], short_term_trendline, label='Short-term trendline')
        ax.plot(df.index[-mid_term_period:], mid_term_trendline, label='Mid-term trendline')
        ax.plot(df.index[-long_term_period:], long_term_trendline, label='Long-term trendline')
        
        ax.legend()
        plt.savefig('plot.png', dpi=300, bbox_inches='tight')
        plt.show()
    
def main():
    stock = Stock()
    stock.name = 'TCS.NS'
    stock.stock()
    
    
if __name__ == '__main__':
    main()