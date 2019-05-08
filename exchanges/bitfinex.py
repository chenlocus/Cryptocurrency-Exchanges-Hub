# coding: utf-8

# In[1]:


# gevent
# bs4
# gunicorn
import os
import requests
import json
import util

data =None
waittime =1


def getSymbol(code):
    symbol_list = util.requestTimeout(url ='https://api.bitfinex.com/v1/symbols',timeout=waittime,errMsg='cannot get symbols in bitfinex!')
    if symbol_list is None:
        return None

    for i in symbol_list.json():
        if i.startswith(code.lower()) & i.endswith('usd'):
            return i
    for i in symbol_list.json():
        if i.startswith(code.lower()) & i.endswith('btc'):
            return i
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol ==None:
        return None

    url = "https://api.bitfinex.com/v1/pubticker/"+symbol

    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get market data from bitfinex')
    if response == None:
        return None

    data = {}
    data['source'] = 'bitfinex'
    data['bid'] = response.json()['bid']
    data['ask'] = response.json()['ask']
    data['trade'] = response.json()['last_price']
    if symbol.endswith('usd'):
        print(data)
        return data
    else:
        response = util.requestTimeout(url='https://api.bitfinex.com/v1/pubticker/btcusd',timout =waittime,
                errMsg='cannot get btcusd in bitfinex')
        if response == None:
            return None
        btc_price = float(response.json()['last_price'])
        data['source'] = 'bitfinex'
        data['bid'] = float(data['bid'])*btc_price
        data['ask'] = float(data['ask'])*btc_price
        data['trade'] = float(data['trade'])*btc_price
        print(data)
        return data