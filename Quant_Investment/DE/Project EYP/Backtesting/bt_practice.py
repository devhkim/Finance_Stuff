from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
import datetime
import os.path
import sys
from datetime import date
from yahoo_fin.stock_info import get_data
import pandas as pd

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy(size = 1)

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size = 1)
                

if __name__ == '__main__' :

    # set today's date
    month = date.today().month
    year = date.today().year
    day = date.today().day

    # get list of stocks
    listofstocks = ['AAPL', 'TSLA', 'GOOG', 'MSFT', 'AMZN']

    # blank list for final value
    final_value = []

    # initial conditions
    cash = 10000.0 # per stock
    commiss = 0.001 # per transaction

    fromyear = 2020
    frommonth = 3
    fromday = 5

    endyear = 2020
    endmonth = 9
    endday = 21

    # create CSV files of each stock
    for alpha in listofstocks:

        # import cerebro engine
        cerebro = bt.Cerebro()
        cerebro.addstrategy(TestStrategy)

        df = pd.DataFrame(get_data(alpha))
        df = df.drop(columns = "ticker")
        df['Date1'] = df.index
        df = df.rename(columns = {'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'adjclose':'Adj Close', 'volume':'Volume'})
        Date = []
        for i in df['Date1']:
            if len(str(i.month)) == 1:
                if len(str(i.day)) == 1:
                    Date.append(str(str(i.year)+"-0"+str(i.month)+"-0"+str(i.day)))
                else:
                    Date.append(str(str(i.year) + "-0" + str(i.month) + "-" + str(i.day)))
            else:
                if len(str(i.day)) == 1:
                    Date.append(str(str(i.year)+"-"+str(i.month)+"-0"+str(i.day)))
                else:
                    Date.append(str(str(i.year) + "-" + str(i.month) + "-" + str(i.day)))

        df['Date'] = Date
        df = df.drop(columns = {'Date1'})
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
        df = df.fillna(method = 'ffill')

        df.to_csv(str(year)+str(month)+str(day)+"_"+alpha+".csv", index = False)

        # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), str(year)+str(month)+str(day)+"_"+stock+".csv")

        # data = bt.feeds.YahooFinanceCSVData(
        #     dataname = datapath,
        #     fromdate = datetime.datetime(2018, 3, 5),
        #     todate = datetime.datetime(2019, 2, 1),
        #     reverse = False)

        cerebro.adddata(bt.feeds.YahooFinanceCSVData(
            dataname = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), str(year)+str(month)+str(day)+"_"+alpha+".csv"),
            fromdate = datetime.datetime(fromyear, frommonth, fromday),
            todate = datetime.datetime(endyear, endmonth, endday),
            reverse = False))

        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission=commiss)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.run()

        print('FInal Portfolio Value: %.2f' % cerebro.broker.getvalue())
        final_value.append(cerebro.broker.getvalue())

    # organize in a dictionary
    dictionary = {}
    for stock in range(len(listofstocks)):
        dictionary[stock] = {'ticker': listofstocks[stock],
                             'starting_value': cash,
                             'ending_value': final_value[stock],
                             'starting_date': datetime.date(fromyear,frommonth, fromday),
                             'ending_date': datetime.date(endyear, endmonth, endday)}

    final_df = pd.DataFrame(dictionary, index = None)
    final_df.to_csv(str(fromyear)+str(frommonth)+str(fromday)+"_to_"+str(endyear)+str(endmonth)+str(endday)+"_backtest.csv")
