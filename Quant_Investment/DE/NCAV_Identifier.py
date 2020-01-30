import pandas as pd
import Quotes_Yahoofin as qy
from yahoo_fin.stock_info import get_income_statement
import datetime as dt
import time

qt = qy.get_German_quotes()
ncav = {}

tickers = qt.DE_tickers("Jan17_CS.csv")

start_time = dt.datetime.now()

count = 0

for i in tickers:
    if count == 100 or count == 200 or count == 300 or count == 400 or count == 500 or count == 600:
        time.sleep(180)
        try:
            df = get_income_statement(i)
            if int(df.loc[df['Breakdown'] == 'Net Income'].iloc[:,1]) >= 0:
                ncav[i] = qt.NCAV(i)
                print(i + " is successfully appended.")
                count += 1
            else:
                print(i + " has negative net income.")
                count += 1
        except:
            print(i + " is N/A.")
            count += 1
    else:
        try:
            df = get_income_statement(i)
            if int(df.loc[df['Breakdown'] == 'Net Income'].iloc[:,1]) >= 0:
                ncav[i] = qt.NCAV(i)
                print(i + " is successfully appended.")
                count += 1
            else:
                print(i + " has negative net income.")
                count += 1
        except:
            print(i + " is N/A.")
            count += 1

ncav = pd.DataFrame(list(ncav.items()), columns = ['Tickers', 'NCAV'])
ncav = ncav.sort_values(by = 'NCAV', ascending = False)

print(ncav)
print(ncav.head(int(len(ncav)*0.05)))
print(count)

end_time = dt.datetime.now()
print(end_time - start_time)
count = 0