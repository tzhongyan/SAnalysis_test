import numpy as np
import pandas as pd
from datetime import datetime

from pandas_datareader import DataReader

class StockAnalyser:
  """
  A basic analyser for analysing latest stock from Yahoo Finance within a timeframe.
  """
  def __init__(self, company_listing):
    self.company_listing = company_listing
    self.__df = pd.DataFrame()
  
  def full_df(self):
    return self.__df
  
  def head(self):
    return self.__df.head()

  def load_csv(self, csv_path):
    if self.__df.empty:
      self.__df = pd.read_csv(csv_path)
    else:
      s = input('There is data in this analyser. Do you still want to continue? [Y/n]')
      if s[0]=='Y' or s[0]=='y':
        self.__df = pd.read_csv(csv_path)
      else:
        pass

  def save_to_csv(self, csv_path):
    if self.__df.empty:
      print('You need to load data into your dataframe before you can save it.')
    else:
      self.__df.to_csv(csv_path)
      print('Data saved to ' + csv_path)

  def load_data_from_yahoo(self, start_date='default', end_date='default'):
    """
      Pull data from Yahoo Finance using pandas_datareader, and save it into self.__df
    """
    # Check if dataframe is empty
    if not self.__df.empty:
      s = input('There is data in this analyser. Do you still want to continue? [Y/n]')
      if s[0]!='Y' and s[0]!='y':
        pass
    
    # If both start_date and end_date are not specified, we will grab data for the past
    # year.
    # If end_date is not specified, we will use now(today) as the end date.
    # If start_date is not specified, we will get data for past 1 year ending at end_date.
    if end_date == 'default':
      end_date = datetime.now()
    if start_date == 'default':
      start_date = datetime(end_date.year-1, end_date.month, end_date.day)
    
    try:
      self.__df = DataReader(self.company_listing, 'yahoo', start_date, end_date)
      print('Data grabbed successfully from Yahoo! Finance. Here\'s a peek')
      self.__df.reset_index(inplace=True)
      print(self.head())
    except:
      raise Exception

  def get_closing(self):
    """
    Returns a DataFrame containing the closing price for each day.
    """
    return self.__df[['Date','Close']]

  def get_volume(self):
    """
    Returns a Series containing the exchange volume for each day.
    """
    return self.__df[['Date','Volume']]
  
  def get_daily_return(self):
    """
    Returns a DataFrame that contains daily return. It is the percentage change of
    today's closing price against last closing price
    """
    # copy close column from df
    df = self.__df[['Date','Close']].copy()
    # shift 1 row down, and store the series as yesterday
    df['last_closing']= df['Close'].shift(1)
    # calculate the percentage change
    df['Daily Return'] = (df['Close'] - df['last_closing']) / df['last_closing']
    # Drops the last_closing and Close columns as they are irrelevant
    df = df.drop(columns=['last_closing', 'Close'])
    return df
  
  def __per_calc(self, a, b):
    return (a-b)/b

  def __calc_moving_average(self, days=10, base='Close'):
    """
    Calculates the moving average for base, and return a Series.
    """
    # Copy the important part from dataframe
    # Note: [[_]] makes it a dataframe copy instead of a series
    df = self.__df[[base]].copy()
    # Shift down the values of base, based on the days defined
    for i in range(days):
      df[i] = df[base].shift(i)
    # After the loop, we have a dataframe which column names contains the number
    # of rolling days, and the base. To calculate the mean, we should remove the
    # base column.
    df = df.drop(columns=['Close'])
    # First few rows will contain NaN after shifting, we are keeping it with
    # skipna=False flag; and axis=1 to calculate mean based on row-wise.
    return df.mean(skipna=False, axis=1)
    
  
  def get_rolling_mean(self, day_list=[5, 10, 15, 20], base='Close'):
    cols = []
    cols.append('Date')
    cols.append(base)
    for day in day_list:
      col_name = 'Moving Average for ' + repr(day) + 'days'
      cols.append(col_name)
      self.__df[col_name] = self.__calc_moving_average(day, base)
    
    return self.__df[cols]
