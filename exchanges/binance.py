
# In[6]:


# gevent
# bs4
# gunicorn
import os
import requests
import json
import util

waittime =1
data =None



def getSymbol(code):
    symbol_list = util.requestTimeout(url='https://api.binance.com/api/v1/exchangeInfo',timeout=waittime,errMsg='cannot get exchangeInfo in binance!')

    if symbol_list == None:
        return None

    for i in symbol_list.json()['symbols']:
        symbol = i['symbol']
        quoteasset= i['quoteAsset']
        if symbol.startswith(code.upper()) & (quoteasset == 'USDT'):
            return symbol
            
    for i in symbol_list.json()['symbols']:
        symbol = i['symbol']
        quoteasset= i['quoteAsset']
        if symbol.startswith(code.upper()) & (quoteasset == 'BTC'):
            return symbol
    
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol ==None:
        return None

    url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=%s"%symbol
    print(url)
    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get bookTicker in binance')
    
    if response is None:
        return None

    data = {}
    data['source'] = 'binance'
    data['bid'] = float(response.json()['bidPrice'])
    data['ask'] = float(response.json()['askPrice'])
    URL = "https://api.binance.com/api/v1/trades" 
    payload = {'symbol': symbol, 'limit':1}
    response = util.requestTimeout(url=URL,timeout=waittime,errMsg='cannot get trade in binance',payload=payload)
    if response is None:
        return None

    data['trade'] = float(response.json()[0]['price'])
    if symbol.endswith('USDT'):
        print(data)
        return data
    else:
        response = util.requestTimeout(url='https://api.binance.com/api/v1/trades?symbol=BTCUSDT&limit=1',timeout=waittime,
            errMsg='cannot get btc usd price in binance')
        
        if response is None:
            return None
        btc_price = float(response.json()[0]['price'])
        data['source'] = 'binance'
        data['bid'] = round(float(data['bid'])*btc_price,4)
        data['ask'] = round(float(data['ask'])*btc_price,4)
        data['trade'] = round(float(data['trade'])*btc_price,4)
        print(data)
        return data
            
    