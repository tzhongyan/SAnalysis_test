from MarketAnalysis import analyser

if __name__ == '__main__':
  c = analyser.StockAnalyser()
  c.grab_data_from_yahoo('bili')
  c.closing_plot()