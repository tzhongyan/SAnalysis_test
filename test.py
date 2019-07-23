import sys
import io
import unittest
import pandas as pd
import numpy as np

from datetime import datetime
from pandas.util.testing import assert_frame_equal, assert_series_equal

from MarketAnalysis import analyser

class TestAnalyser(unittest.TestCase):
  def setUp(self):
    """
    Setup testing environment, we will load the data from input/bili.csv.
    empty_analyse will be used for empty sets;
    bili will load data from input/bili.csv
    """
    self.empty = analyser.StockAnalyser('empty')
    self.bili = analyser.StockAnalyser('BILI')
    self.bili.load_csv('input/bili.csv')
    self.bili_df = self.bili.full_df()

  def test_load_csv(self):
    """
    Tests the load_csv method. If this fails, the entire test
    should fail.
    """
    self.empty.load_csv('input/bili.csv')
    res = pd.read_csv('input/bili.csv')
    res['Date'] = np.vectorize(pd.to_datetime)(res['Date'])
    # assert true if frame equal
    assert_frame_equal(res, self.empty.full_df(),)
  
  # @unittest.skip('skip this when debugging test unit')
  def test_load_data_from_yahoo(self):
    """
    Tests the load_data_from_yahoo method. This will compare the
    test with the prepared bili.csv, i.e. stock of BILI, with
    starting date 2018-07-20 and ending date 2019-07-19.

    Since DataReader also reads data 1 day before start date,
    we should set our start date as 2018-07-21. 
    """
    data = analyser.StockAnalyser('BILI')
    start = datetime(2018,7,21)
    end = datetime(2019,7,19)
    # Setup a text trap to surpress stdout for test
    # Ref: https://codingdose.info/2018/03/22/supress-print-output-in-python/
    text_trap = io.StringIO()
    sys.stdout = text_trap

    data.load_data_from_yahoo(start_date=start, end_date=end)

    # Assert true if dataframe equals.Needs to use check_less_precise
    # as loading float from saved csv could be dodgy.
    assert_frame_equal(self.bili_df, data.full_df(), check_less_precise=3)

  def test_get_daily_return(self):
    """
    Tests get_daily_return method. We can use pandas.Series.pct_change to
    the test the method.
    """
    res = self.bili_df['Close'].pct_change()
    # Obtain df from bili using the method
    test = self.bili.get_daily_return()
    # we will be only testing on 'Daily Return' series against res
    assert_series_equal(res, test['Daily Return'], check_names=False)
  
  def test_rolling_mean(self):
    """
    Tests get_rolling_mean method. We can use pandas.DataFrame.rolling to
    the roll, then mean() to get the rolling mean.
    In this test, we will use 'Close' as base.
    """
    # setup list of days for MA
    day_list = [10, 20, 50, 100]
    # copy bili_df for local result test use
    res = self.bili_df.copy()
    # setup columns required
    cols = []
    cols.append('Date')
    cols.append('Close')
    for day in day_list:
      col_name = 'Moving Average for ' + repr(day) + 'days'
      cols.append(col_name)
      # Using library
      res[col_name] = res['Close'].rolling(day).mean()
    # only taking columns required
    res = res[cols]

    test = self.bili.get_rolling_mean(day_list=day_list, base='Close')

    assert_frame_equal(res,test)
  

if __name__ == '__main__':
  unittest.main()