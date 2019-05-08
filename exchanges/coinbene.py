
# coding: utf-8

# In[6]:



# coding: utf-8

# In[6]:


# gevent
# bs4
# gunicorn
import os
import requests
import json
import util

data =None
waittime =1

#round(x,2)


def getSymbol(code):
    
    symbol_list = util.requestTimeout(url ='http://api.coinbene.com/v1/market/symbol',timeout = waittime,errMsg='cannot get symbol from coinbene')

    if symbol_list is None:
        return None

    for i in symbol_list.json()['symbol']:
        symbol = i['baseAsset']
        quoteasset= i['quoteAsset']
        if (symbol == code) & (quoteasset == 'USDT'):
            return i['ticker']
            
    for i in symbol_list.json()['symbol']:
        symbol = i['baseAsset']
        quoteasset= i['quoteAsset']
        if (symbol==code.upper()) & (quoteasset == 'BTC'):
            return i['ticker']
    
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol == None:
        return None
    
    url = "http://api.coinbene.com/v1/market/ticker?symbol=%s"%symbol
    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get market data from coinbene')
    if response is None:
        return None

    data = {}
    data['source'] = 'coinbene'
    data['bid'] = response.json()['ticker'][0]['bid']
    data['ask'] = response.json()['ticker'][0]['ask']   
    data['trade'] = response.json()['ticker'][0]['last']
    if symbol.endswith('USDT'):
        print(data)
        return data
    else:
        response = util.requestTimeout(url='http://api.coinbene.com/v1/market/ticker?symbol=btcusdt',timeout=waittime,errMsg='cannot get market data from coinbene')
        if response == None:
            return data
        btc_price = float(response.json()['ticker'][0]['last'])
        print (btc_price)
        data['source'] = 'coinbene'
        data['bid'] = round(float(data['bid'])*btc_price,4)
        data['ask'] = round(float(data['ask'])*btc_price,4)
        data['trade'] = round(float(data['trade'])*btc_price,4)
        print(data)
        return data
    
if __name__ == '__main__':   
    symbol = 'XRP'
    data = getUSDPrice(symbol)

