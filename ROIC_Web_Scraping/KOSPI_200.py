import requests
import numpy as np

class kospi_200:

    def kospi200_list(self):
        sourcelist = []
        for i in range(1,22,1):
            url = 'https://finance.naver.com/sise/entryJongmok.nhn?&page=%s'
            url = url % i
            response = requests.get(url)
            response = response.text

            soup = response.splitlines()
            sourcelist.append(soup)

        flat_list = [item for sublist in sourcelist for item in sublist]

        pattern = '\t\t<td class="ctg"><a href="/item/main.nhn?code='

        valuelist = []

        for line in flat_list:
            val = ""
            for i in range(len(line)):
                if i>= len(pattern):
                    val += line[i]
                elif i < len(pattern) and line[i] != pattern[i]:
                    break

            if "<font" in val:
                valuelist.append(val[18:-12])
            elif val != "":
                valuelist.append(val[:-5])

        new_dict = {}

        for stock in self.formatting(valuelist):
            new_dict[stock[0:6]] = stock[25:-4]

        return new_dict

        # return self.formatting(valuelist)
        # return flat_list

    def formatting(self,my_list):
        newlist = []
        for i in range(len(my_list)):
            try:
                if my_list[i] == '-':
                    newlist.append(0)
                elif isinstance(float(my_list[i].replace(",","")),float) == True:
                    newlist.append(float(my_list[i].replace(",","")))
            except:
                newlist.append(my_list[i])
        return newlist

