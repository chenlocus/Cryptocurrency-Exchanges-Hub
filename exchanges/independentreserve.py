
# coding: utf-8

# In[3]:


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
    symbol_list = util.requestTimeout(url='https://api.independentreserve.com/Public/GetValidPrimaryCurrencyCodes',
        timeout=waittime,errMsg='cannot get symbol from independentreserve')
    if symbol_list is None:
        return None
    symbol_list = symbol_list.json()
    symbol_list_lower = [x.lower() for x in symbol_list]
    if code=='BTC':
        return 'xbt'
    else:
        if code.lower() in symbol_list_lower:
            return code.lower()
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol ==None:
        return None

    URL = "https://api.independentreserve.com/Public/GetMarketSummary" 
    payload = {'primaryCurrencyCode': symbol, 'secondaryCurrencyCode':'usd'}
    response = util.requestTimeout(url=URL,payload=payload,timeout=waittime,errMsg='cannot get market data from independentreserve')
    if response is None:
        return None
    data = {}
    data['source'] = 'independentreserve'
    data['bid'] = response.json()['CurrentHighestBidPrice']
    data['ask'] = response.json()['CurrentLowestOfferPrice']
    data['trade'] = response.json()['LastPrice']  
    print(data)
    return data
