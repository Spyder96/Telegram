#!/usr/bin/env python
# coding: utf-8

import ta
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy.stats import linregress


class Stock:

    def __init__(self, name='', interval=365):
        self.ticker = name
        self.data = None
        self.start_date = (datetime.datetime.today() -
                           datetime.timedelta(days=interval)).strftime('%Y-%m-%d')
        self.end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.df = None
        self.short_term_period = None
        self.mid_term_period = None
        self.long_term_period = None

    def get_data(self):
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        self.df = pd.DataFrame(self.data)

    def show_data(self, period=1):
        return self.df.tail(period).T.apply(lambda x: round(x, 2))

    def calculate_technical_indicators(stock, ema_span=9, ema_span_list=None, rsi_window=14, macd_fast=12,
                                       macd_slow=26, macd_signal=9):
        if ema_span_list is None:
            ema_span_list = [20, 50, 100, 200]
        stock.df['EMA{}'.format(ema_span)] = stock.df['Close'].ewm(span=ema_span, adjust=False).mean()
        for span in ema_span_list:
            stock.df['EMA{}'.format(span)] = stock.df['Close'].ewm(span=span, adjust=False).mean()
        stock.df['VolumeAvg20'] = stock.df['Volume'].rolling(window=20).mean()
        stock.df['RSI'] = ta.momentum.RSIIndicator(stock.df['Close'], window=rsi_window).rsi()
        macd = ta.trend.MACD(stock.df['Close'], window_fast=macd_fast, window_slow=macd_slow, window_sign=macd_signal)
        stock.df['MACD'] = macd.macd()
        stock.df['MACD_signal'] = macd.macd_signal()
        stock.df['MACD Above Signal'] = stock.df['MACD'] > stock.df['MACD_signal']

    # Define a function to calculate the slope and y-intercept of a trendline

    def set_period_values(self, st=10, mt=50, lt=100):
        self.short_term_period = st
        self.mid_term_period = mt
        self.long_term_period = lt

    def trendline(self):
        def trend_data(x, y):
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            return slope * x + intercept

        def calculate_trendline(df, period):
            return trend_data(np.arange(len(df['Close']))[-period:], df['Close'][-period:])

        self.short_term_trendline = calculate_trendline(self.df, self.short_term_period)
        self.mid_term_trendline = calculate_trendline(self.df, self.mid_term_period)
        self.long_term_trendline = calculate_trendline(self.df, self.long_term_period)

    # Calculate the short-term trendline using linear regression

    # # Calculate the mid-term trendline using linear regression
    # mid_term_trendline = calculate_trendline(np.arange(len(df['Close']))[-mid_term_period:], df['Close'][-mid_term_period:])

    # # Calculate the long-term trendline using linear regression
    # long_term_trendline = calculate_trendline(np.arange(len(df['Close']))[-long_term_period:], df['Close'][-long_term_period:])

    # # Plot the price data and trendlines
    def plot_trends(self):
        # if self.short_term_trendline == None:
        #     trendline()

        fig, ax = plt.subplots(figsize=(10, 6))

        self.df['Close'].plot(ax=ax, label='Close')
        ax.plot(self.df.index[-self.short_term_period:], self.short_term_trendline, label='Short-term trendline')
        ax.plot(self.df.index[-self.mid_term_period:], self.mid_term_trendline, label='Mid-term trendline')
        ax.plot(self.df.index[-self.long_term_period:], self.long_term_trendline, label='Long-term trendline')

        ax.legend()
        plt.savefig('plot.png', dpi=300, bbox_inches='tight')
        # plt.show()


def main():
    tcs = Stock('TCS.NS')

    tcs.get_data()
    tcs.show_data()
#    tcs.set_period_values()
#    tcs.trendline()
#    tcs.plot_trends()


if __name__ == '__main__':
    main()
