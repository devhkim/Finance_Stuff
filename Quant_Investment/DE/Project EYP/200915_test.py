import key_stats as ks
import pandas as pd
import get_list_of_nyse as nyse
import datetime


now = datetime.datetime.now()

nyse = nyse.find_tickers()
kss = ks.key_stats()

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

# create list for ROA and PER
testlist = nyse_dic["ticker"]
PERlist = []
ROAlist = []

# fill the lists with PER and ROA scraped values
for i in testlist:
    PERlist.append(kss.PER(i))
    ROAlist.append(kss.ROA(i))

# make PER dataframe
PERdic = {}
PERdic['stock'] = stocks
PERdic['ticker'] = tickers
PERdic['PER'] = PERlist

PERdf = pd.DataFrame(PERdic).replace("N/A", 999999)
PERdf = PERdf[PERdf.PER != "not an equity"]
# PERdf = PERdf.sort_values('PER', ascending=True)
# PERdf = PERdf.reset_index()
# PERdf['Rank_PER'] = PERdf.index
# PERdf = PERdf.drop(columns = ['index'])
# PERnumeric = pd.to_numeric(PERdf['Rank_PER'])
# PERdf['Rank_PER'] = PERnumeric

# make ROA dataframe
ROAdic = {}
ROAdic['stock'] = stocks
ROAdic['ticker'] = tickers
ROAdic['ROA'] = ROAlist

ROAdf = pd.DataFrame(ROAdic).replace("N/A", -999999)
ROAdf = ROAdf[ROAdf.ROA != "not an equity"]
# ROAdf = ROAdf.sort_values('ROA', ascending=False)
# ROAdf = ROAdf.reset_index()
# ROAdf['Rank_ROA'] = ROAdf.index
# ROAdf = ROAdf.drop(columns = ['index'])
# ROAnumeric = pd.to_numeric(ROAdf['Rank_ROA'])
# ROAdf['Rank_ROA'] = ROAnumeric

# merge the two tables and rank them
full_df = pd.merge(PERdf, ROAdf, on="ticker", how="outer").drop(columns=['stock_y'])
full_df = full_df.rename(columns={"stock_x": "stock"})
# full_df['Ranks_added'] = full_df.Rank_PER + full_df.Rank_ROA
# full_df = full_df.sort_values('Ranks_added', ascending = True)
full_df["PER_ranks"] = full_df["PER"].rank(ascending = True, method = 'min')
full_df["ROA_ranks"] = full_df["ROA"].rank(ascending = False, method = 'min')
full_df["added_ranks"] = full_df.ROA_ranks + full_df.PER_ranks

full_df["added_ranks"][full_df.ROA == -999999] = None
full_df["added_ranks"][full_df.PER == 999999] = None

print(full_df)

# to csv file (optional)
csvname = 'NYSE_Ranks_'+now.strftime("%Y%m%d-%H%M") + '.csv'
full_df.to_csv('C:\\Users\\Devin\\Desktop\\'+csvname, index = False)

print(str(datetime.datetime.now() - now) + " elapsed")