import os 
import pandas as pd
import numpy as np
import datetime
import math
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import pyfolio as pf
import matplotlib
import matplotlib.pyplot as plt
import bs4 as bs
import requests
import yfinance as yf
import datetime

# Scrape the S&P 500 company list from Wikipedia
resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})
tickers = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker)
tickers = [s.replace('\n', '') for s in tickers]

# Set start and end dates for historical stock prices download
start = datetime.datetime(2010,1,3)
end = datetime.datetime(2020,6,3)

# Download historical stock prices for the S&P 500 companies
data = yf.download(tickers, start=start, end=end)
print(data)

# Save stock data to a CSV file
path = os.getcwd()
FilePathOut = path + '/' + 'data' + '_hist.csv'
data.to_csv(FilePathOut)

# Select a subset of the data related to stock volumes
Volumes = data.iloc[:,2525:3030]

# Pull macroeconomic data from the FRED and Quandl APIs
from fredapi import Fred
fred = Fred(api_key='insert yours here')
M1 = fred.get_series('M1SL')
M2 = fred.get_series('M2SL')
M3 = fred.get_series('MABMM301USM189S')
Effective_Federal_Funds_Rate = fred.get_series('FEDFUNDS')
S10_Year_Treasury_Constant_Maturity_Rate = fred.get_series('GS10')
Three_Month_Treasury_Bill_Secondary_Market_Rate = fred.get_series('TB3MS')
Interest_Rates_Discount_Rate_for_United_States = fred.get_series('INTDSRUSM193N')
Unemployment = fred.get_series('UNRATE')
consumer_price_index = fred.get_series('CPIAUCSL')
non_financial_corporate_debt = fred.get_series('BCNSDODNS')

# Resample the data to monthly data
data.resample('m').mean()

# Load financial data for US companies from the SimFin API
import simfin as sf
from simfin.names import *

# Set API-key for downloading data
sf.set_api_key('free')

# Set the local directory where data-files are stored
sf.set_data_dir('~/simfin_data/')

# Load the full list of companies in the US
df_companies = sf.load_companies(market='us')

# Load all the industries that are available
df_industries = sf.load_industries()

# Load the quarterly Income Statements for all US companies
df_income = sf.load_income(variant='quarterly', market='us')

# Load the quarterly Balance Sheet data for all US companies
df_balance = sf.load_balance(variant='quarterly', market='us')

# Load the quarterly Cash Flow data for all US companies
df_cashflow = sf.load_cashflow(variant='quarterly', market='us')

# Perform data analysis and visualization
clean = adjonly[~adjonly.isin([np.nan, np.inf, -np.inf,1]).any(1)]
boxing=pd.DataFrame()
boxing['mean_daily_returns_of_all_stocks']=clean.mean(axis=1)
boxing = boxing[boxing.mean_daily_returns_of_all_stocks != -1]
ax= boxing.boxplot()

ax.set_title('Box Plot Of Mean Daily Log Returns')
ax.set_ylabel('Log Returns')

plt.hist(boxing['mean_daily_returns_of_all_stocks'],bins=190)
plt.title('Histogram of Log Returns Of All Stocks')
plt.ylabel('Number of Observations')
plt.xlabel('Log Return Value')
plt.show()

frames = [M1, M2, M3, Manufacturing_Composite_Index, AAII_Investor_Sentiment_Data, University_of_Michigan_Consumer_Survey_Index_of_Consumer_Sentiment, NMI_Non_Manufacturing_Index, Effective_Federal_Funds_Rate, S10_Year_Treasury_Constant_Maturity_Rate, Three_Month_Treasury_Bill_Secondary_Market_Rate, Interest_Rates_Discount_Rate_for_United_States, Unemployment, consumer_price_index]
macrodata = pd.DataFrame()
macrodata = pd.concat(frames, axis=1)
macrodata.columns = ['M1', 'M2', 'M3', 'Manufacturing_Composite_Index', 'Bullish', 'Bearish', 'neutral', 'University_of_Michigan_Consumer_Survey_Index_of_Consumer_Sentiment', 'NMI_Non_Manufacturing_Index', 'Effective_Federal_Funds_Rate', 'S10_Year_Treasury_Constant_Maturity_Rate', 'Three_Month_Treasury_Bill_Secondary_Market_Rate', 'Interest_Rates_Discount_Rate_for_United_States', 'Unemployment', 'consumer_price_index']
macrodata1 = macrodata.fillna(0)

path = os.getcwd()
FilePathOut = path + '/' + 'Macrodata' + '_hist.csv'
macrodata1.to_csv(FilePathOut)

plt.plot(S10_Year_Treasury_Constant_Maturity_Rate)
plt.title('S&P 500 10-Year Treasury Constant Maturity Rate')
plt.ylabel('Rate')

# Plotting the interest rates
plt.plot(Effective_Federal_Funds_Rate, label='Effective Federal Funds Rate')
plt.plot(S10_Year_Treasury_Constant_Maturity_Rate, label='10-Year Treasury Rate')
plt.plot(Three_Month_Treasury_Bill_Secondary_Market_Rate, label='3-Month Treasury Bill Rate')
plt.plot(Interest_Rates_Discount_Rate_for_United_States, label='Discount Rate')
plt.legend(loc='best')
plt.title('Interest Rates Over Time')
plt.ylabel('Rate')
plt.show()

# Plotting the unemployment rate
plt.plot(Unemployment)
plt.title('Unemployment Rate Over Time')
plt.ylabel('Rate')
plt.show()

# Plotting the consumer price index
plt.plot(consumer_price_index)
plt.title('Consumer Price Index Over Time')
plt.ylabel('Index Value')
plt.show()

# Plotting the macroeconomic variables
macrodata1.plot(subplots=True, figsize=(12, 18))
plt.suptitle('Macroeconomic Variables Over Time')
plt.show()


