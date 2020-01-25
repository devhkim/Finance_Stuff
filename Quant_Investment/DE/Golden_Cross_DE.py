import Quotes_Yahoofin as qy
import datetime as dt

qt = qy.get_German_quotes()

tickers = qt.DE_tickers("Jan17_CS.csv")

des_tck = []

start_time = dt.datetime.now()

for i in tickers:
    try:
        ma_L = qt.get_ma(i, 20, 90, "1d")
        ma_L = [i for i in ma_L if str(i) != "nan"]
        ma_S = qt.get_ma(i, 5, 90, "1d")
        ma_S = [i for i in ma_S if str(i) != "nan"]

        if ma_L[0]*0.98 <= ma_S[0] and ma_S[0] <= ma_L[0]*1.001 and \
            ma_S[0]/ma_S[5] > ma_L[0]/ma_L[5] and \
            ma_L[0]/ma_L[7] > 1.005 and \
            len(ma_L) >= 90:
            # len(get_data(i + ".DE", interval="1d")['close']) >= 90:
            # np.average(ma_L[0:10]) > np.average(ma_L[11:20]) > np.average(ma_L[21:]) and \
            # np.average(ma_S[0:10]) > np.average(ma_S[11:20]) > np.average(ma_S[21:]) and \

            des_tck.append(i)
            print(i + " crosses the golden bridge")
            print(len(des_tck))

        elif ma_L[0] <= ma_S[0] and ma_S[0] <= ma_L[0]*1.01 and \
            ma_L[3] > ma_S[3] and \
            ma_S[0]/ma_S[5] > ma_L[0]/ma_L[5] and \
            ma_L[0]/ma_L[7] > 1.005 and \
            len(ma_L) >= 90:
            # ma_L[0] / ma_L[10] > 1 and \
            # ma_S[0] / ma_S[3] > ma_L[0] / ma_L[3] and \

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