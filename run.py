from MarketAnalysis.analyser import StockAnalyser
from MarketAnalysis.plot import plot, fancy_plot, plot_histogram

if __name__ == '__main__':
  AAPL = StockAnalyser('AAPL')
  AAPL.load_data_from_yahoo()
  plot(AAPL.get_closing())
  plot(AAPL.get_volume())
  plot(AAPL.get_rolling_mean())

  fancy_plot(AAPL.get_daily_return())
  plot_histogram(AAPL.get_daily_return())
