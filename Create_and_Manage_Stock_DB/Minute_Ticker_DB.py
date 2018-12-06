import sqlite3
import pandas as pd

class Stock_DB(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            return cls._instance
        return cls._instance

    def __init__(self):
        self.open_Db()

    # open the Database
    def open_Db(self):
        self.con = sqlite3.connect("./stockinfo.db")
        self.cursor = self.con.cursor()

    def create_StockDb(self):
        self.cursor.execute("CREATE TABLE portfolio_min(date text str, ticker str, stock str, close int, low int, key unique);")
        self.cursor.execute("CREATE TABLE portfolio_day(date text str, ticker str, stock str, start int, end int, key unique);")

    def insert_port_min(self,day,ticker, stock, close,low, key):
        self.cursor.execute("insert into portfolio_min values(?,?,?,?,?,?);",(day,ticker, stock, close,low, key))

    def insert_port_day(self,day,ticker, stock, start,end, key):
        self.cursor.execute("insert into portfolio_day values(?,?,?,?,?,?);",(day,ticker, stock, start,end, key))

    def select_mindata(self,day):
        data = pd.read_sql("SELECT * FROM portfolio_min where date like \'"+day+"%\' order by date;", self.con, index_col=None)
        return data

    def select_daydata(self,start,end):
        data = pd.read_sql("SELECT * FROM portfolio_day where date >= \'" + start + "\' and date <= \'"+ end +"\';", self.con, index_col=None)
        return data

    def commit(self):
        self.con.commit()

if __name__ == "__main__":
    db = Stock_DB()
    db.create_StockDb()