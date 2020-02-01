import pandas as pd
import Quotes_Yahoofin as qy
from yahoo_fin.stock_info import get_cash_flow
import datetime as dt
import time

qt = qy.get_German_quotes()
kpi = {}
gear = []
per = []
ocash = []
icash = []
fcash = []
ncav = []
mcap = []


tickers = qt.DE_tickers("Jan17_CS.csv")
# tickers = ['AAPL', 'MSFT', '005930.KS']
start_time = dt.datetime.now()

count = 0

for i in tickers:
    if count == 15 or count == 30 or count == 45 or count == 60 or count == 75 or count == 90 or count == 105 or \
        count == 120 or count == 135 or count == 150 or count == 165 or count == 180 or count == 195 or count == 210 or \
        count == 225 or count == 240 or count == 255 or count == 270 or count == 285 or count == 300 or count == 315 or \
        count == 330 or count == 345 or count == 360 or count == 375 or count == 390 or count == 405 or count == 420 or \
        count == 435 or count == 450 or count == 465 or count == 480 or count == 495 or count == 510 or count == 525 or \
        count == 540 or count == 555 or count == 570 or count == 585 or count == 600 or count == 615 or count == 630 or \
        count == 645 or count == 660 or count == 675 or count == 690:
        time.sleep(180)
        try:
            gear.append(qt.gearing(i))
            print(i + " gearing is successfully appended.")
        except:
            gear.append("n.a.")
            print(i + " gearing is N/A.")
        try :
            per.append(qt.per(i))
            print(i + " PER is successfully appended")
        except:
            per.append("n.a.")
            print(i + " PER is N/A.")
        try :
            ocash.append(int(get_cash_flow(i).loc[get_cash_flow(i)['Breakdown'] == "Net cash provided by operating activites"].iloc[:,1]))
            print(i + " operating cash flow is successfully appended")
        except:
            ocash.append("n.a.")
            print(i + " operating cash flow is N/A.")
        try:
            icash.append(int(get_cash_flow(i).loc[get_cash_flow(i)['Breakdown'] == "Net cash used for investing activites"].iloc[:,1]))
            print(i + " investing cash flow is successfully appended")
        except:
            icash.append("n.a.")
            print(i + " investing cash flow is N/A.")
        try:
            fcash.append(int(get_cash_flow(i).loc[get_cash_flow(i)['Breakdown'] == "Net cash used privided by (used for) financing activities"].iloc[:, 1]))
            print(i + " financing cash flow is successfully appended")
        except:
            fcash.append("n.a.")
            print(i + " financing cash flow is N/A.")
        try :
            ncav.append(qt.NCAV(i))
            print(i + " NCAV is successfully appended")
        except:
            ncav.append("n.a.")
            print(i + " NCAV is N/A.")
        try :
            mcap.append(qt.market_cap(i))
            print(i + " market cap is successfully appended")
            count += 1
        except:
            mcap.append("n.a.")
            print(i + " market cap is N/A.")
            count += 1
    else:
        try:
            gear.append(qt.gearing(i))
            print(i + " gearing is successfully appended.")
        except:
            gear.append("n.a.")
            print(i + " gearing is N/A.")
        try :
            per.append(qt.per(i))
            print(i + " PER is successfully appended")
        except:
            per.append("n.a.")
            print(i + " PER is N/A.")
        try :
            ocash.append(int(get_cash_flow(i).loc[get_cash_flow(i)['Breakdown'] == "Net cash provided by operating activites"].iloc[:,1]))
            print(i + " operating cash flow is successfully appended")
        except:
            ocash.append("n.a.")
            print(i + " operating cash flow is N/A.")
        try:
            icash.append(int(get_cash_flow(i).loc[get_cash_flow(i)['Breakdown'] == "Net cash used for investing activites"].iloc[:,1]))
            print(i + " investing cash flow is successfully appended")
        except:
            icash.append("n.a.")
            print(i + " investing cash flow is N/A.")
        try:
            fcash.append(int(get_cash_flow(i).loc[get_cash_flow(i)['Breakdown'] == "Net cash used privided by (used for) financing activities"].iloc[:, 1]))
            print(i + " financing cash flow is successfully appended")
        except:
            fcash.append("n.a.")
            print(i + " financing cash flow is N/A.")
        try :
            ncav.append(qt.NCAV(i))
            print(i + " NCAV is successfully appended")
        except:
            ncav.append("n.a.")
            print(i + " NCAV is N/A.")
        try :
            mcap.append(qt.market_cap(i))
            print(i + " market cap is successfully appended")
            count += 1
        except:
            mcap.append("n.a.")
            print(i + " market cap is N/A.")
            count += 1

kpi['Tickers'] = tickers
kpi['Gearing'] = gear
kpi['PER'] = per
kpi['OpCash'] = ocash
kpi['InvCash'] = icash
kpi['FinCash'] = fcash
kpi['MarketCap'] = mcap
kpi['NCAV'] = ncav

kpi = pd.DataFrame(kpi)
kpi.to_csv('C:\\Users\\Devin\\Documents\\Financial_Data_Cluster\\test.csv')

print(kpi)
# print(ncav.head(int(len(ncav)*0.05)))
print(count)

end_time = dt.datetime.now()
print(end_time - start_time)
count = 0