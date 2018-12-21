
# coding: utf-8

# In[6]:


# gevent
# bs4
# gunicorn
import os
import requests
import json

def getSymbol(code):
    symbol_list = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    
    for i in symbol_list.json()['symbols']:
        symbol = i['symbol']
        if symbol.startswith(code.upper()) & symbol.endswith('USDT'):
            return symbol
#         elif symbol.startswith(code.upper())&symbol.endswith('BTC'):
#             return symbol
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol ==None:
        return None
    print (symbol)
    url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=%s"%symbol
    response = requests.get(url)
    data = {}
    data['source'] = 'binance'
    data['bid'] = round(float(response.json()['bidPrice']),4)
    data['ask'] = round(float(response.json()['askPrice']),4)
    URL = "https://api.binance.com/api/v1/trades" 
    payload = {'symbol': symbol, 'limit':1}
    response = requests.get(url=URL,params=payload)
    data['trade'] = round(float(response.json()[0]['price']),4)
    if symbol.endswith('USDT'):
        return data
    else:
        response = requests.get('https://api.binance.com/api/v1/trades?symbol=BTCUSDT&limit=1')
        btc_price = float(response.json()[0]['price'])
        data['source'] = 'binance'
        data['bid'] = round(float(data['bid'])*btc_price,4)
        data['ask'] = round(float(data['ask'])*btc_price,4)
        data['trade'] = round(float(data['trade'])*btc_price,4)
        print(data)
        return data
    
