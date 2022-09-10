#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import bs4
import json

while True:    
    # dateList = ['20220723', '20220722', '20220721']
    input_string = input('◆ 請輸入日期：')

    dateList = input_string.split()
    print('\n計算中...')

    bet01dataList = []
    bet01DictDataListObj = {}
    
    bet03dataList = []
    bet03DictDataListObj = {}

    for date in dateList:
        r = requests.get('https://www.playsport.cc/predictgame.php?action=result&allianceid=1&gametime=' + date)

        if r.status_code == 200:
        #   print(r.text)

            soup = bs4.BeautifulSoup(r.text, 'lxml')

            bet01Tags = soup.findAll('td', {'class': 'td-bank-bet01'})
            bet03Tags = soup.findAll('td', {'class': 'td-bank-bet03'})
            
            for bet01 in bet01Tags:
                try:
                    bet01dataList.append(
                        ('勝' if bet01.div.get('class') else '') + bet01.div.strong.string + bet01.div.span.strong.string + bet01.div.span.span.string
                    )
                except:
                    continue
                    
                
            for bet03 in bet03Tags:
                try:
                    bet03dataList.append(
                        ('勝' if bet03.div.get('class') else '') + bet03.div.strong.string + bet03.div.span.span.string
                    )
                except:
                    continue
                
        #     print(json.dumps(bet01dataList, indent = 4, ensure_ascii = False))
        #     print(json.dumps(bet03dataList, indent = 4, ensure_ascii = False))

    for bet01data in bet01dataList:
        if '勝' in bet01data:
            if bet01data[1:] not in bet01DictDataListObj:
                bet01DictDataListObj[bet01data[1:]] = 1
            else:
                bet01DictDataListObj[bet01data[1:]] += 1

    for bet03data in bet03dataList:
        if '勝' in bet03data:
            if bet03data[1:] not in bet03DictDataListObj:
                bet03DictDataListObj[bet03data[1:]] = 1
            else:
                bet03DictDataListObj[bet03data[1:]] += 1

    print('\n顯示結果...') 
    print('--------------------------------------------')
    print('讓分：')
    print(json.dumps(bet01DictDataListObj, indent = 4, ensure_ascii = False))

    print('\n不讓分：')
    print(json.dumps(bet03DictDataListObj, indent = 4, ensure_ascii = False))
    print('--------------------------------------------\n\n')    


# In[ ]:





# In[ ]:




