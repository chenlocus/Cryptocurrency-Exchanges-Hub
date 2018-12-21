
# coding: utf-8

# In[1]:


# gevent
# bs4
# gunicorn
import os
import requests
import json

#round(x,2)
def getSymbol(code):
    symbol_list = requests.get('https://api.btcmarkets.net/v2/market/active')
    
    for i in symbol_list.json()['markets']:
        symbol = i['instrument']
        if code == symbol:
            return symbol        
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    print (symbol)
    if symbol == None:
        return None
    url = "https://api.btcmarkets.net/market/%s/AUD/tick"%symbol
    response = requests.get(url)
    data = {}
    data['source'] = 'BTCMarkets'
    data['bid'] = response.json()['bestBid']
    data['ask'] = response.json()['bestAsk']
    data['trade'] = response.json()['lastPrice']
    
    response = requests.get('http://free.currencyconverterapi.com/api/v5/convert?q=AUD_USD&compact=y')
    exchange_rate = float(response.json()['AUD_USD']['val'])
    data['bid'] = round(float(data['bid'])*exchange_rate,4)
    data['ask'] = round(float(data['ask'])*exchange_rate,4)
    data['trade'] = round(float(data['trade'])*exchange_rate,4)
    return data
    
                
symbol = 'BTC'
data = getUSDPrice(symbol)
print(data)


# In[9]:


# gevent
# bs4
# gunicorn
#https://github.com/BTCMarkets/API/wiki/Market-data-API
import os
import requests

URL = "https://api.btcmarkets.net/v2/market/active" 
response = requests.get(URL)
print(response.url)
print(response.json()['markets'])


# In[10]:


import os
import requests

URL = "https://api.btcmarkets.net/market/BTC/AUD/tick" 
response = requests.get(URL)
print(response.url)
print(response.json())

