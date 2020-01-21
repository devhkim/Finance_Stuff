from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs

class find_fs:
    # !/usr/bin/env python
    # -*- coding: utf-8 -*-
    """
        collect_korea_stock_in_fnguide.py
        Fn 데이터 가이드 사이트
        .
    """

    def get_html_fnguide(self, ticker, gb):
        """
        :param ticker: 종목코드
        :param gb: 데이터 종류 (0 : 재무제표, 1 : 재무비율, 2: 투자지표)
        :return:
        """
        url = []

        url.append(
            "https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701")
        url.append(
            "https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701")
        url.append(
            "https://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701")

        if gb > 2:
            return None

        url = url[gb]
        try:

            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html_text = urlopen(req).read()

        except (AttributeError, HTTPError) as e:
            return None

        return html_text

    def ext_fin_fnguide_data(self, ticker, gb, item, n, freq="a"):
        """
        :param ticker: 종목코드
        :param gb: 데이터 종류 (0 : 재무제표, 1 : 재무비율, 2: 투자지표)
        :param item: html_text file에서 원하는 계정의 데이터를 가져온다.
        :param n: 최근 몇 개의 데이터를 가져 올것인지
        :param freq: 'a' : 연간재무, 'q' : 분기재무
        :return: item의 과거 데이터
        """

        html_text = self.get_html_fnguide(ticker, gb)

        soup = bs(html_text, "html.parser")

        d = soup.find_all(text=item)

        if (len(d) == 0):
            return None

        # 최근 4년치를 가져온다.
        nlimit = 4

        if n > nlimit:
            return None
        if freq == 'a':
            # 연간 데이터
            d_ = d[0].find_all_next(class_="r", limit=nlimit)
            # 분기 데이터
        elif freq == 'q':
            d_ = d[1].find_all_next(class_="r", limit=nlimit)
        else:
            d_ = None

        try:
            data = d_[(nlimit-n):nlimit]
            v = [v.text for v in data]

        except (AttributeError, HTTPError) as e:
            return None

        return (v)

    def multiples(self, ticker, gb, item):
        """
        :param ticker: 종목코드
        :param gb: 데이터 종류 (0 : 재무제표, 1 : 재무비율, 2: 투자지표)
        :param item: html_text file에서 원하는 계정의 데이터를 가져온다.
        :return: item의 과거 데이터

        :param item : PBR(Price Book-value Ratio), PER(Price Earning Ratio), 업종 PER, 배당수익률
        """

        html_text = self.get_html_fnguide(ticker, gb)

        soup = bs(html_text, "html.parser")

        d = soup.find_all(text=item)

        if (len(d) == 0):
            return None

        elif (len(d) != 0) :
            d_ = d[0].find_all_next("dd")

        else:
            d_ = None

        try:
            v = [v.text for v in d_]

        except (AttributeError, HTTPError) as e:
            return None

        return (v[1])

    def market_cap(self, ticker, n):
        """
        :param ticker: 종목코드
        :return: 시가총액 값
        """

        html_text = self.get_html_fnguide(ticker, 2)

        soup = bs(html_text, "html.parser")

        d = soup.find_all(text="시가총액")

        if (len(d) == 0):
            return None

        # 최근 1년치를 가져온다.
        nlimit = 10

        if n > nlimit:
            return None
        elif n < nlimit:
            d_ = d[0].find_all_next(class_="r", limit=nlimit)
        else:
            d_ = None

        try:
            data = d_[(nlimit-n):nlimit]
            v = [v.text for v in data]

        except (AttributeError, HTTPError) as e:
            return None

        return (v)

if __name__ == "__main__":
    fn = find_fs()
    ff = fn.ext_fin_fnguide_data("078070", 2, "EPS", 4, freq="a")
    fs = fn.ext_fin_fnguide_data("078070",2,"DPS(보통주,현금)", 4, freq="a")
    # print(float(ff.replace(",",""))>2)
    # print(float(ff[0].replace(",","")))
    # print(type(float(fs[2].replace(",",""))))

    print(fs.index(fs[-1]))