
# coding: utf-8

# In[16]:



# coding: utf-8

# In[6]:


# gevent
# bs4
# gunicorn
import os
import requests
import json
import util

waittime =2


def getSymbol(code):
    return 'USD-'+code

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    url = "https://bittrex.com/api/v1.1/public/getticker?market=%s"%symbol
    response = util.requestTimeout(url=url,timeout = waittime,errMsg='cannote get market data in bittrex')
    if response == None:
        return None
    if response.json()['result'] ==None:
        return None
    data = {}
    data['source'] = 'bittrex'
    data['bid'] = response.json()['result']['Bid']
    data['ask'] = response.json()['result']['Ask']
    data['trade'] = response.json()['result']['Last']
    print(data)
    return data

if __name__ == '__main__':        
    symbol = 'ETH'
    data = getUSDPrice(symbol)
    print(data)

