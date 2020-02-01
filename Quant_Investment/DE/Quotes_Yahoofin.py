import pandas as pd
from yahoo_fin.stock_info import get_data
from yahoo_fin.stock_info import get_balance_sheet
from yahoo_fin.stock_info import get_quote_table
from yahoo_fin.stock_info import get_cash_flow

class get_German_quotes:
    # def __init__(self):
    #     DE = pd.read_csv("Xetra\Jan17.csv") # make sure to update directory in case new file has been downloaded

    def DE_tickers(self, DE):
        germany = pd.read_csv(DE)
        germany = germany[["Instrument", "Mnemonic"]]
        germany["ticker"] = [str(germany["Mnemonic"][i])+".DE" for i in range(len(germany["Mnemonic"]))]
        return list(germany["ticker"])

    def get_ma(self, tck, period, datapoints, iv):
        # tck: ticker
        # period: ma_XX
        # datapoints: number of days/weeks/months of observation
        # iv: interval (1wk, 1mo, 1d)
        # output: spits out the most recent datapoints first

        quotes = get_data(tck, interval = iv)["close"]
        ma = []
        for i in range(datapoints):
            ma.append(quotes[(len(quotes)-period-i):(len(quotes)-i)].mean())
        return ma

    def market_cap(self, tck):
        mc = get_quote_table(tck)['Market Cap']
        if mc[-1] == 'M':
            mc = int(float(mc[:-1])*1000000)
            return mc
        if mc[-1] == 'B':
            mc = int(float(mc[:-1])*1000000000)
            return mc
        if mc[-1] == 'T':
            mc = int(float(mc[:-1])*1000000000000)
            return mc
        else:
            return mc

    def NCAV(self, tck):
        df = get_balance_sheet(tck)
        NCAV_last = (int(df.loc[df['Breakdown'] == 'Total Current Assets'].iloc[:,1]) - \
                     int(df.loc[df['Breakdown'] == 'Total Liabilities'].iloc[:,1]))*1000 / \
                    self.market_cap(tck)
        return NCAV_last

    def per(self, tck):
        per = float(get_quote_table(tck)['PE Ratio (TTM)'])
        return per

    def gearing(self, tck):
        equity = int(get_balance_sheet('AAPL').loc[get_balance_sheet('AAPL')['Breakdown'] == "Total stockholders' equity"].iloc[:,1])
        debt = int(get_balance_sheet('AAPL').loc[get_balance_sheet('AAPL')['Breakdown'] == "Total Liabilities"].iloc[:,1])
        gear = debt/equity
        return gear

    def oif_cash(self, tck):
        cf = []
        oc = int(get_cash_flow('AAPL').loc[get_cash_flow('AAPL')['Breakdown'] == "Net cash provided by operating activites"].iloc[:,1])
        ic = int(get_cash_flow('AAPL').loc[get_cash_flow('AAPL')['Breakdown'] == "Net cash used for investing activites"].iloc[:,1])
        fc = int(get_cash_flow('AAPL').loc[get_cash_flow('AAPL')['Breakdown'] == "Net cash used privided by (used for) financing activities"].iloc[:,1])
        cf.append(oc, ic, fc)
        return cf
