import yahoo_dividend as yd
import get_list_of_nyse as nyse
import datetime
import pandas as pd

now = datetime.datetime.now()

ydd = yd.dividend_data()
nyse = nyse.find_tickers()

nyse_dic = {}
stocks = []
tickers = []

for alpha in nyse.alphabet:
    website = nyse.create_url(alpha)
    dictionary = nyse.scrape_stocks(website)
    stocks.append(dictionary['stock'])
    tickers.append(dictionary['ticker'])

stocks = [item for sublist in stocks for item in sublist]
tickers = [item for sublist in tickers for item in sublist]

nyse_dic['stock'] = stocks
nyse_dic['ticker'] = tickers
candi = []

for i in nyse_dic['ticker']:
    d = ydd.div_tracker(i, 15, 20)
    candi.append(d)
    print(i + " is a " + d)

nyse_dic['divtrack'] = candi

csvname = 'NYSE_dividends_'+now.strftime("%Y%m%d-%H%M") + '.csv'
pd.DataFrame(nyse_dic).to_csv('C:\\Users\\Devin\\Desktop\\NYSE_listing\\div\\'+csvname, index = False)

print(str(datetime.datetime.now() - now) + " elapsed")