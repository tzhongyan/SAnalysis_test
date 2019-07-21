# A wrapper for plotting graph for matplotlib
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot(ss, legend=True, figsize=(15,5)):
  ss.set_index('Date', inplace=True)
  ss.plot(legend=legend, figsize=figsize)
  plt.show(block=True)

def fancy_plot(ss, legend=True, figsize=(15,5), linestyle='--', marker='o'):
  ss.set_index('Date', inplace=True)
  ss.plot(legend=legend, figsize=figsize, linestyle=linestyle, marker=marker)
  plt.show(block=True)

def plot_histogram(ss, bins=100):
  ss.set_index('Date', inplace=True)
  ss.hist(bins=bins)
  plt.show(block=True)