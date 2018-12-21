
# coding: utf-8

# In[1]:


# gevent
# bs4
# gunicorn
import os
import requests
import json


def getSymbol(code):
    symbol_list = requests.get('https://api.bitfinex.com/v1/symbols')
    for i in symbol_list.json():
        if i.startswith(code.lower()):
            if i.endswith('usd'):
                return i
            elif i.endswith('btc'):
                return i
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    print (symbol)
    if symbol ==None:
        return None
    url = "https://api.bitfinex.com/v1/pubticker/"+symbol
    response = requests.get(url)
    data = {}
    data['source'] = 'bitfinex'
    data['bid'] = response.json()['bid']
    data['ask'] = response.json()['ask']
    data['trade'] = response.json()['last_price']
    if symbol.endswith('usd'):
        return data
    else:
        response = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
        btc_price = response.json()['last_price']
        data['source'] = 'bitfinex'
        data['bid'] = data['bid']*btc_price
        data['ask'] = data['ask']*btc_price
        data['trade'] = data['trade']*btc_price
        return data
    
                
symbol = 'BNT'
data = getUSDPrice(symbol)
print(data)

