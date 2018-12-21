
# coding: utf-8

# In[3]:


# gevent
# bs4
# gunicorn
import os
import requests
import json

#round(x,2)
def getSymbol(code):
    symbol_list = requests.get('https://api.independentreserve.com/Public/GetValidPrimaryCurrencyCodes')
    symbol_list = symbol_list.json()
    symbol_list_lower = [x.lower() for x in symbol_list]
    if code=='BTC':
        return 'xbt'
    else:
        if code.lower() in symbol_list_lower:
            print(code.lower())
            return code.lower()
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    print (symbol)
    if symbol ==None:
        return None
    URL = "https://api.independentreserve.com/Public/GetMarketSummary" 
    payload = {'primaryCurrencyCode': symbol, 'secondaryCurrencyCode':'usd'}
    response = requests.get(URL,params=payload)
    data = {}
    data['source'] = 'independentreserve'
    data['bid'] = response.json()['CurrentHighestBidPrice']
    data['ask'] = response.json()['CurrentLowestOfferPrice']
    data['trade'] = response.json()['LastPrice']  
    return data