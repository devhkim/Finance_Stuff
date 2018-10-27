import pandas as pd
import numpy as np
import pandas_datareader as web
from datetime import datetime as dt
from matplotlib import pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time

# extract data

TR_REQ_TIME_INTERVAL = 0.2

class stockdata(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = stockdata()
    kiwoom.comm_connect()

    kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

    # opt10081 TR 요청
    kiwoom.set_input_value("종목코드", "005380")
    kiwoom.set_input_value("기준일자", time.strftime("%Y%m%d"))
    kiwoom.set_input_value("수정주가구분", 1)
    kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

    while kiwoom.remained_data == True:
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", "005380")
        kiwoom.set_input_value("기준일자", time.strftime("%Y%m%d"))
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

    df = pd.DataFrame(kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=kiwoom.ohlcv['date'])

# Technical Indicator Function

def t_ind(quotes, tgt_margin = 0.025, n_days = 10) :
    v = (quotes['close'] + quotes['high'] + quotes['low'])/3
    h = v[:-n_days]
    r = pd.DataFrame(np.zeros((len(h), n_days)))
    r[0] = list(h[0:])
    for i in range(n_days-1) :
        if len(v[i+1:]) > len(v[n_days:]) :
            r[i+1] = list(v[i+1:len(h)+1+i])
        else :
            r[i+1] = list(v[i+1:])
    for i in range(n_days-1) :
            r[i+1] = (r[i+1]/r[0])-1
    r[0] = 0
    for i in range(n_days) :
        r.loc[abs(r[i]) < tgt_margin, i] = 0
    r['ind'] = r.sum(axis=1)
    return r['ind']

# 3 month amount of data
df3 = df[-53:]

# plot the hlc and technical indicator

plt.figure(1)
plt.subplot(211)
plt.plot((df3['close']+df3['high']+df3['low'])/3)

plt.locator_params(axis='both',nbins=10)

plt.subplot(212)
plt.plot(t_ind(df3))
plt.show()

TR_REQ_TIME_INTERVAL = 0.2

