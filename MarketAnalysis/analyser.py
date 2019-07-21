import numpy as np
import pandas as pd
from datetime import datetime

from pandas_datareader import DataReader

# Data Visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline
import matplotlib
matplotlib.use('TkAgg')

class StockAnalyser:
  """
  An wrapper for analysing latest stock from Yahoo Finance within a timeframe.
  """
  def __init__(self):
    self.company_name = ''
    self.__df = pd.DataFrame()
  
  def load_csv(self, csv_path):
    if self.__df != pd.DataFrame():
      self.__df = pd.read_csv(csv_path)
    else:
      print('There is data in this analyser.')
  
  def save_to_csv(self, csv_path):
    if self.__df.empty:
      print('You need to load data into your dataframe before you can save it.')
    else:
      self.__df.to_csv(csv_path)
      print('Data saved to ' + csv_path)

  def grab_data_from_yahoo(self, company_listing, start_date='default', end_date='default'):
    """
      Pull data from Yahoo Finance using pandas_datareader, and save it into self.__df
    """
    # If start and end date are not specified, we will grab data from the past 1 year
    # If start date is not specified, we will get data for past 1 year;
    # whilst end date is not specified, we will use now as the end date.
    if end_date == 'default':
      end_date = datetime.now()
    if start_date == 'default':
      start_date = datetime(end_date.year-1, end_date.month, end_date.day)
    
    try:
      self.__df = DataReader(company_listing, 'yahoo', start_date, end_date)
      print('Data grabbed successfully from Yahoo! Finance. Here\'s a peek')
      print(self.__df.head())
    except:
      raise Exception

  def closing_plot(self):
    self.__df['Close'].plot(legend=True, figsize=(15,5))
    plt.show(block=True)
