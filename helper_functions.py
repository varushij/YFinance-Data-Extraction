import yfinance as yf
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def get_tickers():
    '''
    List of currency pairs to be used for analysis
    Output: list of currency pairs
    '''
    currency_tickers = ['AUDCAD=X','AUDCHF=X','AUDJPY=X','AUDNZD=X','AUDUSD=X','CADCHF=X','CADJPY=X','CHFJPY=X',
                    'EURAUD=X','EURCAD=X','EURCHF=X','EURGBP=X','EURJPY=X','EURNZD=X','EURUSD=X','GBPAUD=X',
                    'GBPCAD=X','GBPCHF=X','GBPJPY=X','GBPNZD=X','GBPUSD=X','NZDCAD=X','NZDCHF=X','NZDJPY=X',
                    'NZDUSD=X','USDCAD=X','USDCHF=X','USDJPY=X']
    return currency_tickers

def clean_df(ticker_df,ticker):
    '''
    Set datetime columns and add ticker name for each entry
    Input: dataframe,string
    Output: dataframe
    '''
    ticker_df = ticker_df.reset_index()
    ticker_df.insert(loc=0, column ='Ticker', value=ticker)
    return ticker_df

def get_5min(ticker):
    '''
    Get ticker data for 5 minutes interval and append to df_5min
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='1d', interval = '5m')
    final_df = clean_df(data,ticker)
    return final_df

def get_15min(ticker):
    '''
    Get ticker data for 15 minutes interval and append to df_15min
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='1d', interval = '15m')
    final_df = clean_df(data,ticker)
    return final_df

def get_30min(ticker):
    '''
    Get ticker data for 30 minutes interval and append to df_30min
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='1d', interval = '30m')
    final_df = clean_df(data,ticker)
    return final_df

def get_60min(ticker):
    '''
    Get ticker data for 60 minutes interval and append to df_60min
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='1d', interval = '60m')
    final_df = clean_df(data,ticker)
    return final_df

def get_1day(ticker):
    '''
    Get ticker data for 1 day interval and append to df_1day
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='1d', interval = '1d')
    final_df = clean_df(data,ticker)
    return final_df

def get_1week(ticker):
    '''
    Get ticker data for 1 week interval and append to df_1week
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='1d', interval = '1wk')
    final_df = clean_df(data,ticker)
    return final_df

def get_1month(ticker):
    '''
    Get ticker data for 1 month interval and append to df_1month
    Input: string
    Output: dataframe
    '''
    data = yf.download(tickers = ticker, period ='3mo', interval = '1mo')
    final_df = clean_df(data,ticker)
    return final_df

def connect_postgres():
    '''
    Function to create Postgres connection for performing UPSERT
    Output: connection string
    '''
    conn = psycopg2.connect("dbname=DATABASENAME user=USERNAME host=HOST password=PASSWORD port=PORT")
    conn.autocommit = True
    return conn

def connect_sqlalchemy():
    '''    Function to create sqlalchemy connection for creating temporary tables
    Output: engine connection string
    '''
    engine = create_engine('postgresql+psycopg2://USERNAME:PASSWORD@HOST:PORT/DATABASENAME')
    return engine
