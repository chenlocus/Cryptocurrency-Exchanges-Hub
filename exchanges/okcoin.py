
# coding: utf-8

# In[4]:



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



def getSymbol(code):
    code_list =['btc_usd','ltc_usd','eth_usd','etc_usd','bch_usd']
    symbol =code.lower()+'_'+'usd'
    if symbol in code_list:
        return symbol
    else:
        return None
    

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol ==None:
        return None

    url = "https://www.okcoin.com/api/v1/ticker.do?symbol=%s"%symbol
    response = util.requestTimeout(url=url,timeout =waittime,errMsg='cannot get market data from okcoin')
    if response is None:
        return None

    data = {}
    data['source'] = 'OKcoin'
    data['bid'] = response.json()['ticker']['buy']
    data['ask'] = response.json()['ticker']['sell']
    data['trade'] = response.json()['ticker']['last']
    print(data)
    return data
    

if __name__ == '__main__': 
    symbol = 'LTC'
    data = getUSDPrice(symbol)
    print(data)

