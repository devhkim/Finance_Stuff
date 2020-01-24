import Quotes_Yahoofin as qy
import datetime as dt

qt = qy.get_German_quotes()

tickers = qt.DE_tickers("Jan17_CS.csv")

des_tck = []

start_time = dt.datetime.now()

for i in tickers:
    try:
        ma_30 = qt.get_ma(i, 20, 90, "1d")
        ma_30 = [i for i in ma_30 if str(i) != "nan"]
        ma_10 = qt.get_ma(i, 5, 90, "1d")
        ma_10 = [i for i in ma_10 if str(i) != "nan"]

        if ma_30[0]*0.98 <= ma_10[0] and ma_10[0] <= ma_30[0]*1.001 and \
            ma_10[0]/ma_10[5] > ma_30[0]/ma_30[5] and \
            ma_30[0]/ma_30[7] > 1.005 and \
            len(ma_30) >= 90:
            # len(get_data(i + ".DE", interval="1d")['close']) >= 90:
            # np.average(ma_30[0:10]) > np.average(ma_30[11:20]) > np.average(ma_30[21:]) and \
            # np.average(ma_10[0:10]) > np.average(ma_10[11:20]) > np.average(ma_10[21:]) and \

            des_tck.append(i)
            print(i + " crosses the golden bridge")
            print(len(des_tck))

        elif ma_30[0] <= ma_10[0] and ma_10[0] <= ma_30[0]*1.01 and \
            ma_30[3] > ma_10[3] and \
            ma_10[0]/ma_10[5] > ma_30[0]/ma_30[5] and \
            ma_30[0]/ma_30[7] > 1.005 and \
            len(ma_30) >= 90:
            # ma_30[0] / ma_30[10] > 1 and \
            # ma_10[0] / ma_10[3] > ma_30[0] / ma_30[3] and \

            des_tck.append(i)
            print(i + " crosses the golden bridge")
            print(len(des_tck))

        else:
            print(i + " crosses nothing")

    except:
        print(i + " N/A")

print(des_tck)
print(len(des_tck))

end_time = dt.datetime.now()
print(end_time - start_time)