import datetime as dt
from datetime import datetime as dtt, timedelta
from bs4 import BeautifulSoup
import requests
import collections

class dividend_data:

    def __init__(self):
        self.date_format = "%m/%d/%Y"

    def get_today_unix(self):
        now = dt.datetime.now()
        beg = dtt.strptime('1/1/1970', self.date_format)
        delta = now-beg
        unix = delta.days*24*60*60
        return unix

    def unix_to_date(self, unix):
        beg = dtt.strptime('1/1/1970', self.date_format)
        days = unix/24/60/60
        date = beg + timedelta(days)
        return date.strftime("%Y-%m-%d")

    def build_url(self, today, tckr):
        return "https://finance.yahoo.com/quote/" + tckr + \
               "/history?period1=0&period2=" + str(today) + "&interval=div%7Csplit&filter=div&frequency=1d"

    def getIndexPositions(self, listOfElements, element):
        ''' Returns the indexes of all occurrences of give element in
        the list- listOfElements '''

        indexPosList = []
        indexPos = 0
        while True:
            try:
                # Search for item in list from indexPos to the end of list
                indexPos = listOfElements.index(element, indexPos)
                # Add the index position in list
                indexPosList.append(indexPos)
                indexPos += 1
            except ValueError as e:
                break
        return indexPosList

    def flatten(self, x):
        if isinstance(x, collections.Iterable):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]

    def checksameorgreater(self, list1, val):
        # traverse in the list
        for x in list1:
            # compare with all the values
            # with val
            if val > x:
                return 'False'
        return 'True'

    def get_dividend(self, url):
        pr = requests.get(url, timeout = 5)
        pc = BeautifulSoup(pr.content, "html.parser")
        splitlist = str(pc.findAll('script')[30]).split(',')
        div = [i for i in splitlist if i[0:8] == '{"amount']
        index_amount = []
        index_date = []
        for i in div:
            if div.count(i) < 2:
                index_amount.append(splitlist.index(i))
                index_date.append(splitlist.index(i)+1)
            else:
                index_amount.append(self.getIndexPositions(splitlist, i))
                index_date.append([x+1 for x in self.getIndexPositions(splitlist, i)])
        temp_amount = []
        temp_date = []
        for x in index_amount:
            if x not in temp_amount:
                temp_amount.append(x)
            else:
                pass
        for y in index_date:
            if y not in temp_date:
                temp_date.append(y)
            else:
                pass
        amount = self.flatten(temp_amount)
        date = self.flatten(temp_date)
        amount1 = [float(splitlist[i][10:]) for i in amount]
        date1 = [self.unix_to_date(int(splitlist[i][7:])) for i in date]
        dic = {}
        dic['amount'] = amount1
        dic['date'] = date1
        temp = []
        if len(dic['amount']) > len(dic['date']):
            for j in range(len(dic['date'])):
                temp.append(str(dic['date'][j])+'|'+str(dic['amount'][j]))
        else:
            for j in range(len(dic['amount'])):
                temp.append(str(dic['date'][j])+'|'+str(dic['amount'][j]))
        res = []
        for i in temp:
            if i not in res:
                res.append(i)
            else:
                pass
        res1 = [item for sublist in [i.split('|') for i in res] for item in sublist]
        amount1 = [float(i) for i in res1[1::2]]
        date1 = [dtt.strptime(j, "%Y-%m-%d").strftime("%Y-%m-%d") for j in res1[0::2]]
        dic1 = {}
        dic1['amount'] = amount1
        dic1['date'] = date1
        return dic1

    def div_tracker(self, tckr, yr, divhistory):
        try:
            base = self.get_dividend(self.build_url(self.get_today_unix(), tckr))
            # removing the most recent year and the oldest year
            years = [dtt.strptime(i,"%Y-%m-%d").year for i in base['date'] if dtt.strptime(i,"%Y-%m-%d").year != dtt.today().year and
                     dtt.strptime(i,"%Y-%m-%d").year != dtt.strptime(base['date'][-1], "%Y-%m-%d").year]
            # the company must have given out dividends at least in the last X years
            if years.count(years[0]) == 12 and len(years) >= 12*yr and len(years) >= 12*divhistory:
                toindex = 12*yr
            elif years.count(years[0]) == 12 and len(years) < 12*yr and len(years) >= 12*divhistory:
                toindex = len(years)
            elif years.count(years[0]) == 4 and len(years) >= 4*yr and len(years) >= 4*divhistory:
                toindex = 4*yr
            elif years.count(years[0]) == 4 and len(years) < 4 * yr and len(years) >= 4*divhistory:
                toindex = len(years)
            elif years.count(years[0]) == 2 and len(years) >= 2* yr and len(years) >= 2*divhistory:
                toindex = 2*yr
            elif years.count(years[0]) == 2 and len(years) < 2* yr and len(years) >= 2*divhistory:
                toindex = len(years)
            elif years.count(years[0]) == 1 and len(years) >= 1* yr and len(years) >= 1*divhistory:
                toindex = yr
            elif years.count(years[0]) == 1 and len(years) < 1* yr and len(years) >= 1*divhistory:
                toindex = len(years)
            else:
                toindex = 0
            div_counts = [years.count(years[i]) for i in range(len(years[0:toindex]))]
            # check if there has been any year in which dividend payment was skipped (base year: last year)
            counter = 0
            value_adder = 0
            if self.checksameorgreater(div_counts, div_counts[0]) == 'True':
                while counter <= len(div_counts):
                    if base['amount'][counter]>=base['amount'][counter+1]:
                        counter += 1
                        value_adder += 1
                    else:
                        counter += 1
                        value_adder += 0
                if value_adder == counter:
                    return "candidate"
                else:
                    return "non-candidate"
            else:
                return "non-candidate"
        except:
            return "non-candidate"

    def get_divmonth(self, tckr, payments):
        base = self.get_dividend(self.build_url(self.get_today_unix(), tckr))
        months = [dtt.strptime(i, "%Y-%m-%d").month for i in base['date'][0:payments]]
        return ", ".join(map(str, sorted(set(months))))