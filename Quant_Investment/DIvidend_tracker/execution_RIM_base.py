import key_stats as ks
import yahoo_dividend as yd
from pathlib import Path
import pandas as pd
import datetime

now = datetime.datetime.now()

kss = ks.key_stats()
months = yd.dividend_data()

dd = kss.find_latest_csv("C:\\Users\\Devin\\Desktop\\NYSE_listing\\div\\")
df = (pd.read_csv(dd))
candi = df['divtrack'] == 'candidate'
candidate = df[candi].reset_index(drop=True)
dic = {}
dic['stock'] = list(candidate['stock'])
dic['ticker'] = list(candidate['ticker'])

dic['divratio'] = [kss.get_dividend_yield(i) for i in dic['ticker']]
dic['ROE'] = [kss.get_latest_ROE(i) for i in dic['ticker']]
dic['marketcap'] = [kss.marketcap(i) for i in dic['ticker']]
dic['equity'] = [kss.total_equity(i) for i in dic['ticker']]
dic['shares_outstanding'] = [kss.shares(i) for i in dic['ticker']]
dic['closing_price'] = [kss.previousclose(i) for i in dic['ticker']]
dic['div_months'] = [months.get_divmonth(i, 40) for i in dic['ticker']]

csvname = 'NYSE_RIM_'+now.strftime("%Y%m%d-%H%M") + '.csv'
pd.DataFrame(dic).to_csv('C:\\Users\\Devin\\Desktop\\NYSE_listing\\div\\'+csvname, index = False)

print(str(datetime.datetime.now() - now) + " elapsed")