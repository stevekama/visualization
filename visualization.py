import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from zigzag import *
import ipywidgets as widgets

# This is not nessessary to use zigzag. 
# It's only here so that
# this example is reproducible.
np.random.seed(1997)

X = np.cumprod(1 + np.random.randn(100) * 0.01)
pivots =    peak_valley_pivots(X, 0.03, -0.03)

def plot_pivots(X, pivots):
    plt.xlim(0, len(X))
    plt.ylim(X.min()*0.99, X.max()*1.01)
    plt.plot(np.arange(len(X)), X, 'k:', alpha=0.5)
    plt.plot(np.arange(len(X))[pivots != 0], X[pivots != 0], 'k-')
    plt.scatter(np.arange(len(X))[pivots == 1], X[pivots == 1], color='g')
    plt.scatter(np.arange(len(X))[pivots == -1], X[pivots == -1], color='r')

plot_pivots(X, pivots)

modes = pivots_to_modes(pivots)
pd.Series(X).pct_change().groupby(modes).describe().unstack()

compute_segment_returns(X, pivots)

max_drawdown(X)

def plot_peak(val):
  print("Current Stock: ", val)
  F = get_data_yahoo(val)
  X = get_data_yahoo(val)['Adj Close']
  pivots = peak_valley_pivots(X.values, 0.05, -0.05)
  ts_pivots = pd.Series(X, index=X.index)
  ts_pivots = ts_pivots[pivots != 0]
  X.plot()
  ts_pivots.plot(style='g-o', figsize=(10, 10))

def plot_peak(val):
  print("Current Stock: ", val)
  F = get_data_yahoo(val)
  X = get_data_yahoo(val)['Adj Close']
  pivots = peak_valley_pivots(X.values, 0.05, -0.05)
  ts_pivots = pd.Series(X, index=X.index)
  ts_pivots = ts_pivots[pivots != 0]
  X.plot()
  ts_pivots.plot(style='g-o', figsize=(10, 10))


#I wnt an Intereactive Graph For this one

#I want A dropdown menu that contains a list of all, Stock Codes available on Yahoo Finance
#and it will change the get_yahhoo data 
def dropdown_eventhandler(change):
    print(change.new)

from pandas_datareader import get_data_yahoo
#Add all other stock present in yahoo finance.
experiment_widget = widgets.Dropdown(
        options=['AAPL', 'GOOG'],
        value='AAPL',
        description='Experiments: '
    )
experiment_widget.observe(dropdown_eventhandler, names='value')
display(experiment_widget)

#Since the dataset is in daily, I want to have on option where I can change the timeframe
timewidget = widgets.Dropdown(
        options=['DAILY', 'WEEKLY', 'YEARLY'],
        value='YEARLY',
        description='TIMEFRAME: '
    )
timewidget.observe(dropdown_eventhandler, names='value')
display(timewidget)


#Whenevery a value is change from the widget, i want the graph/visualization to change also
plot_peak(experiment_widget.value)

mavg_7= F['Close'].rolling(window=7).mean()
mavg_30= F['Close'].rolling(window=30).mean()
#Add This moving averages on the plot
#I want to have a checkbox where I can disable and enable which one to hide and which one to show

date = ts_pivots.index #date is the datetime index
date = date.strftime('%Y-%m-%d') #this will return you a numpy array, element is string.
dstr = date.tolist() #
print(dstr)

#I want this calculated Commulative Volume to be show on the Graph Above.
#So that when I hover my mouse it will show
sum_of_low_to_high = []
sum_of_high_to_low = []
for i in range(0, len(dstr) -1):
    #print(dstr[i])
    print("Volume From: ", dstr[i] , " to", dstr[i + 1])
    summ = F[dstr[i]: dstr[i + 1]]['Volume'].sum()
    print("Cummulative Volume: ", summ)
    if i == 0 or i % 2 == 0:
        ##This is from low to high
        sum_of_low_to_high.append(summ)
    else:
        sum_of_high_to_low.append(summ)

print("*****************************************************")

uptrend_volume =sum(sum_of_low_to_high)
downtrend_volume = sum(sum_of_high_to_low)
print("Sum of Uptrends: ",uptrend_volume )
print("Sum of Downtrends: ", downtrend_volume)

diff_uptrend_lowtrend = uptrend_volume - downtrend_volume
print("Difference Between UpTrend and LowTrend Volume: ", diff_uptrend_lowtrend)