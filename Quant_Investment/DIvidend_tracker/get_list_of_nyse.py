from bs4 import BeautifulSoup
import requests
import pandas as pd

class find_tickers:

    def __init__(self):
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def create_url(self, key):
        return "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies="+key

    def scrape_stocks(self, url):
        links = []
        page_response = requests.get(url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        for i in page_content.find_all('a', href=True):
            links.append(str(i))
        new = [f for f in [i for i in links if i[0:14] == '<a href="https'] if f.find('img src') == -1]
        dic = {}
        name = []
        ticker = []
        for j in range(len(new[0::2])):
            name.append(new[0::2][j][new[0::2][j].index('">')+2:new[0::2][j].index('</a>')])
        for z in range(len(new[1::2])):
            ticker.append(new[1::2][z][new[1::2][z].index('">') + 2:new[1::2][z].index('</a>')])
        dic['stock'] = name
        dic['ticker'] = ticker

        return dic