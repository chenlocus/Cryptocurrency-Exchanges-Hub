
# coding: utf-8

# In[14]:


import os
import requests
import json
from datetime import datetime

def getHistoricalData(symbol,interval):
    if interval == 'day':
        url = "https://min-api.cryptocompare.com/data/histohour?fsym=%s&tsym=USD&limit=24"%symbol
    elif interval =='month':
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=USD&limit=30"%symbol
    elif interval =='3 months':
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=USD&limit=90"%symbol
    elif interval == 'year':
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=USD&limit=365"%symbol
    response = requests.get(url)
    data_list =[]
    for x in response.json()['Data']:
        data = {}
        data['close'] = x['close']
        data['time'] = datetime.fromtimestamp(x['time']).strftime('%Y-%m-%d,%H:%M')
#         data['high'] = x['high']
#         data['low'] = x['low']
#         data['open'] = x['open']
        data_list.append(data)
    return data_list


