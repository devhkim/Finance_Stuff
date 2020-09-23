import get_list_of_nyse as get
from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd

now = datetime.datetime.now()

# import the class to fetch equity list from NYSE
nyse = get.find_tickers()

# prepare empty dictionary, lists for the output
nyse_dic = {}
stocks = []
tickers = []

# get the stock names and tickers
for alpha in nyse.alphabet:
    website = nyse.create_url(alpha)
    dictionary = nyse.scrape_stocks(website)
    stocks.append(dictionary['stock'])
    tickers.append(dictionary['ticker'])

stocks = [item for sublist in stocks for item in sublist]
tickers = [item for sublist in tickers for item in sublist]

nyse_dic['stock'] = stocks
nyse_dic['ticker'] = tickers

csvname = 'NYSE_listing_'+now.strftime("%Y%m%d-%H%M") + '.csv'
pd.DataFrame(nyse_dic).to_csv('C:\\Users\\Devin\\Desktop\\NYSE_listing\\'+csvname, index = False)

print(str(datetime.datetime.now() - now) + " elapsed")
