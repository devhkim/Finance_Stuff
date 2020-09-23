import requests
from bs4 import BeautifulSoup
from pathlib import Path

class key_stats:

    def get_url(self, ticker):
        return "https://finance.yahoo.com/quote/" + ticker + "/key-statistics?p=" + ticker

    def get_balancesheetURL(self, ticker):
        return "https://finance.yahoo.com/quote/" + ticker + "/balance-sheet?p=" + ticker

    def get_summaryURL(self, ticker):
        return "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker

    def parse(self, ticker):
        url = self.get_url(ticker)
        pr = requests.get(url, timeout=5)
        pc = BeautifulSoup(pr.content, "html.parser")
        return [str(i) for i in pc]

    def parse_bs(self, ticker):
        url = self.get_balancesheetURL(ticker)
        pr = requests.get(url, timeout=5)
        pc = BeautifulSoup(pr.content, "html.parser")
        return [str(i) for i in pc]

    def parse_summary(self, ticker):
        url = self.get_summaryURL(ticker)
        pr = requests.get(url, timeout=5)
        pc = BeautifulSoup(pr.content, "html.parser")
        return [str(i) for i in pc]

    def get_latest_ROE(self, ticker):
        try:
            parsed = self.parse(ticker)
            ROEstr = "".join(parsed)
            ROElist = ROEstr.split(",")
            ROEpre = [j for j in ROElist if j[0:16] == '"returnOnEquity"']
            ROE = ROEpre[0][24:]
            return float(ROE)
        except:
            return "N/A"

    def get_dividend_yield(self, ticker):
        try:
            parsed = self.parse(ticker)
            string = "".join(parsed)
            list = string.split(",")
            pre = [j for j in list if j[0:29] == '"trailingAnnualDividendYield"']
            final = pre[0][37:]
            return float(final)
        except:
            return "N/A"

    def total_equity(self, ticker):
        try:
            parsed = self.parse_bs(ticker)
            string = "".join(parsed)
            list = string.split(",")
            pre = [j for j in list if j[0:24] == '"totalStockholderEquity"']
            final = pre[0][32:]
            return int(final)
        except:
            return "N/A"

    def shares(self, ticker):
        try:
            parsed = self.parse(ticker)
            string = "".join(parsed)
            list = string.split(",")
            pre = [j for j in list if j[0:19] == '"sharesOutstanding"']
            final = pre[0][27:]
            return int(final)
        except:
            return "N/A"

    def marketcap(self, ticker):
        try:
            parsed = self.parse_summary(ticker)
            string = "".join(parsed)
            list = string.split(",")
            pre = [j for j in list if j[0:11] == '"marketCap"']
            final = pre[-6][19:]
            return int(final)
        except:
            return "N/A"

    def PER(self, ticker):
        if self.quotetype(ticker) == "EQUITY":
            try:
                parsed = self.parse_summary(ticker)
                string = "".join(parsed)
                list = string.split(",")
                pre = [j for j in list if j[0:12] == '"trailingPE"']
                final = pre[0][20:]
                return float(final)
            except:
                return "N/A"
        else:
            return "not an equity"

    def ROA(self, ticker):
        if self.quotetype(ticker) == "EQUITY":
            try:
                parsed = self.parse_summary(ticker)
                string = "".join(parsed)
                list = string.split(",")
                pre = [j for j in list if j[0:16] == '"returnOnAssets"']
                final = pre[0][24:]
                return float(final)
            except:
                return "N/A"
        else:
            return "not an equity"

    def quotetype(self, ticker):
        try:
            parsed = self.parse_summary(ticker)
            string = "".join(parsed)
            list = string.split(",")
            pre = [j for j in list if j[0:11] == '"quoteType"']
            final = pre[0]
            return final[13:].replace('"',"")
        except:
            return "N/A"

    def previousclose(self, ticker):
        try:
            parsed = self.parse_summary(ticker)
            string = "".join(parsed)
            list = string.split(",")
            pre = [j for j in list if j[0:28] == '"regularMarketPreviousClose"']
            final = pre[0][36:]
            return float(final)
        except:
            return "N/A"

    def find_latest_csv(self, path):
        # need to import Path from pathlib before use
        files = Path(path).glob('*.csv')

        latest = max(files, key=lambda f: f.stat().st_mtime)

        return latest