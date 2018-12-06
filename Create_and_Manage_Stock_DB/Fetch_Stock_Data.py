import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import Minute_Ticker_DB


class Stock(QAxWidget):
    def __init__(self):
        super().__init__()
        self.db = Minute_Ticker_DB.Stock_DB()
        self.db.open_Db()

        self._create_kiwoom_instance()
        self._set_signal_slots()

    # Method to use COM
    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        # OnEventConnect upon login
        self.OnEventConnect.connect(self._event_connect)
        # Event after tr
        self.OnReceiveTrData.connect(self._receive_tr_data)

    # Event Loop
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    # Login Successful?
    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")
        self.login_event_loop.exit()

    # input tr
    # ex. SetInputValue("종목코드","000660")
    def set_input_value(self,id,value):
        self.dynamicCall("SetInputValue(QString,QString)", id, value)

    # tr to server
    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    # get data from server
    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    # count data from server
    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):

        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10080_req":
            self._opt10080(rqname, trcode)
        elif rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

        print("receive_tr_data call")

    # request stock data by minute
    # ca. 100 days
    def req_minute_data(self):
        self.set_input_value("종목코드",tckr)
        self.set_input_value("틱범위", 1)
        self.set_input_value("수정주가구분", 0)
        self.comm_rq_data("opt10080_req", "opt10080", 0, "1999")

        for i in range(30):
            time.sleep(0.5)
            self.set_input_value("종목코드",tckr)
            self.set_input_value("틱범위", 1)
            self.set_input_value("수정주가구분", 0)
            self.comm_rq_data("opt10080_req", "opt10080", 2, "1999")

        print(tckr + " " + "minute data saved")

    # request daily stock data.
    def req_day_data(self):
        self.set_input_value("종목코드",tckr)
        self.set_input_value("기준일자", "20181206")
        self.set_input_value("수정주가구분",0)
        self.comm_rq_data("opt10081_req", "opt10081",0,"2000")

        print(tckr + " " + "daily data saved")

    # load saved minute data to portfolio_min
    def _opt10080(self,rqname,trcode):
        data_cnt = self._get_repeat_cnt(trcode,rqname)
        for i in range(data_cnt):
            try:
                day = self._comm_get_data(trcode, "",rqname, i, "체결시간")
                close = self._comm_get_data(trcode, "", rqname, i, "현재가")
                low = self._comm_get_data(trcode, "", rqname, i, "저가")
                if(close[0] == '-'):
                    close = close[1:]
                if(low[0] == '-'):
                    low = low[1:]
                self.db.insert_port_min(day, tckr, stck, int(close),int(low), day+stck+tckr)
                print("saving minute data")
            except:
                pass

        self.db.con.commit()

    # load saved daily data to portfolio_day
    def _opt10081(self,rqname, trcode):
        for i in range(150):
            try:
                day = self._comm_get_data(trcode, "",rqname, i, "일자")
                end = self._comm_get_data(trcode, "",rqname, i,"현재가")
                start = self._comm_get_data(trcode, "",rqname, i,"시가")
                self.db.insert_port_day(day, tckr, stck, int(start), int(end), day+stck+tckr)
                print("saving daily data")
            except:
                pass
        self.db.commit()


if __name__ == "__main__":
    ticker_stock = {
                    'ticker': ["005930", "005380",
                                "068270", "047810", "159580"],
                    'stock': ["삼성전자", "현대자동차",
                               "셀트리온", "한국항공우주", "제로투세븐"]
                    }
    app = QApplication(sys.argv)
    stock = Stock()
    stock.comm_connect()

    for i in range(len(ticker_stock['ticker'])):
        tckr = ticker_stock['ticker'][i]
        stck = ticker_stock['stock'][i]

        stock.req_minute_data()
        stock.req_day_data()