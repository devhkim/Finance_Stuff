import pandas as pd
from KOSPI_200 import *
from ROIC_Addressed import *
import time

start = time.time()
print(start)

kospi_list = kospi_200()
roiclist = fetch_financials()

stocks = list(kospi_list.kospi200_list().values())
tickers = list(kospi_list.kospi200_list().keys())

roic_2013 = []
roic_2014 = []
roic_2015 = []
roic_2016 = []
roic_2017 = []

for ticker in tickers:
    roic_value = roiclist.calc_roic(ticker)
    roic_2013.append(roic_value[0])
    roic_2014.append(roic_value[1])
    roic_2015.append(roic_value[2])
    roic_2016.append(roic_value[3])
    roic_2017.append(roic_value[4])

d = {'Ticker':tickers,
     'Stock':stocks,
     '2013-12-31':roic_2013,
     '2014-12-31':roic_2014,
     '2015-12-31':roic_2015,
     '2016-12-31':roic_2016,
     '2017-12-31':roic_2017}

df = pd.DataFrame(data=d)

df.to_excel('C:/Users/Devin/KOSPI_ROIC.xlsx', sheet_name='sheet1', index=False)

end = time.time()
print(end)
print(end - start)