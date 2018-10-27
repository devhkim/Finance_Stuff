import requests
import numpy as np

class fetch_financials:

    def get_list(self, ticker):
        url = 'http://media.kisline.com/investinfo/mainInvestinfo.nice?paper_stock=%s&nav=3'
        url = url % (ticker)
        response = requests.get(url)
        response = response.text

        soup = response.splitlines()

        pattern = '\t\t\t\t\t\t<td class="rgt">'
        pattern2 = '\t\t\t\t\t\t<th scope="row">'
        valuelist = []

        for line in soup:
            val = ""
            for i in range(len(line)):
                if i>= len(pattern):
                    val += line[i]
                elif i < len(pattern) and line[i] != pattern[i]:
                    if line[i] == pattern2[i] :
                        val += line[i]
                    else :
                        break

            if "<font" in val:
                valuelist.append(val[18:-12])
            elif val != "":
                valuelist.append(val[:-5])

        return self.formatting(valuelist)
        # return soup

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

    def calc_roic(self, ticker):
        dff = self.get_list(ticker)

        # ROIC
        try:
            roic_index = [i for i, x in enumerate(dff) if x == "hscopeow투자자본수익률(ROIC)"]
            roic = [(dff[roic_index[0]+1]),(dff[roic_index[0]+3]), (dff[roic_index[0]+5]), (dff[roic_index[0]+7]), (dff[roic_index[0]+9])]
        except:
            roic = [None, None, None, None, None]

        return roic



