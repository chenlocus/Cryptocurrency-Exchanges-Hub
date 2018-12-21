
# coding: utf-8

# In[16]:


# gevent
# bs4
# gunicorn
import os
import requests
import json

def getUSDPrice(symbol):
    symbol = symbol.upper()+'-USDT'
    print(symbol)
    if symbol ==None:
        return None
    url = "https://www.okex.com/api/spot/v3/instruments/ticker"
    
    response = requests.get(url)
    
    for x in response.json():
        if x['instrument_id']==symbol:
            data = {}
            data['source'] ='okex'
            data['bid'] = x['best_bid']
            data['ask'] = x['best_ask']
            data['trade'] = x['last']
            return data
    return None
    
code = 'eos'
data = getUSDPrice(code)
print(data)

