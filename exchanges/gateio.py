
# coding: utf-8

# In[8]:



# coding: utf-8

# In[6]:


# gevent
# bs4
# gunicorn
import os
import requests
import json
import util

waittime =1

#round(x,2)




def getUSDPrice(symbol):
    symbol = symbol.lower()+'_'+'usdt'
    url = "https://data.gateio.io/api2/1/ticker/%s"%symbol
    response = util.requestTimeout(url=url, timeout =waittime,errMsg='cannot get market data from gateio')
    if response == None:
        return None
    data = {}
    data['source'] = 'gateio.io'
    try:
        data['bid'] = response.json()['highestBid']
        data['ask'] = response.json()['lowestAsk']
        data['trade'] = response.json()['last']
        print(data)
        return data
    except:
        return None

    symbol = symbol.lower()+'_'+'btc'
    url = "https://data.gateio.io/api2/1/ticker/%s"%symbol
    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get market data from gateio')
    if response is None:
        return None

    data = {}
    data['source'] = 'gateio.io'
    try:
        data['bid'] = response.json()['highestBid']
        data['ask'] = response.json()['lowestAsk']
        data['trade'] = response.json()['last']
    except:
        return None
    response = util.requestTimeout(url='https://data.gateio.io/api2/1/ticker/btc_usdt',timeout=waittime,errMsg='cannot get market data from gateio')
    try:
        btc_price = float(response.json()['price'])
    except:
        return None
        
    data['bid'] = float(data['bid'])*btc_price
    data['ask'] = float(data['ask'])*btc_price
    data['trade'] = float(data['trade'])*btc_price
    print(data)
    return data
        
if __name__ == '__main__':        
    symbol = 'ETH'
    data = getUSDPrice(symbol)
    print(data)

