
# coding: utf-8

# In[16]:


# gevent
# bs4
# gunicorn
import os
import requests
import json
import util

data =None
waittime =1



def getUSDPrice(symbol):
    symbol = symbol.upper()+'-USDT'
    if symbol ==None:
        return None

    url = "https://www.okex.com/api/spot/v3/instruments/ticker"
    
    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get market data from okex')

    if response == None:
        return None
    
    for x in response.json():
        if x['instrument_id']==symbol:
            data = {}
            data['source'] ='okex'
            data['bid'] = x['best_bid']
            data['ask'] = x['best_ask']
            data['trade'] = x['last']
            print(data)
            return data

    return None

if __name__ == '__main__':
    code = 'eos'
    data = getUSDPrice(code)
    print(data)

