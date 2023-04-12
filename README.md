# Macro-Economic-Data-and-Stock-Data-for-Data-Analysis-and-Visualization

This Python code uses several libraries to download and analyze financial and macroeconomic data. It first uses the requests and BeautifulSoup libraries to scrape a Wikipedia page for a list of companies in the S&P 500 index. It then uses the yfinance library to download historical stock prices for the companies in the index and saves the data to a CSV file.

The code then selects a subset of the downloaded data, representing the trading volumes of the companies, and calculates the average daily volume for each company. It sorts the companies by their average volume and saves the results to a CSV file.

The code then uses the quandl library to download several macroeconomic indicators, such as the M1 and M2 money supply, interest rates, and unemployment rate. It also uses the fredapi library to download data from the Federal Reserve Economic Data (FRED) database, such as the Consumer Price Index (CPI).

Next, the code uses the pandas library to clean and merge the financial and macroeconomic data. It resamples the data to create monthly and daily frequency data, and it fills any missing values using forward filling. It then creates several plots to visualize the data, such as a box plot of the mean daily log returns of all the stocks, a histogram of the log returns, and line charts of the interest rates, unemployment rate, consumer price index, and macroeconomic variables over time.

Finally, the code uses the simfin library to download financial data for US companies, such as income statements, balance sheets, and cash flow statements. It loads the data into pandas dataframes and performs some basic analysis and visualization.

Overall, this Python code provides a framework for downloading, cleaning, and analyzing financial and macroeconomic data, and it can be used as a starting point for more advanced financial analysis projects.
