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
    symbol_list = util.requestTimeout(url='https://api.independentreserve.com/Public/GetValidPrimaryCurrencyCodes',
        timeout=waittime,errMsg='cannot get symbol from independentreserve')



def getSymbol(code):
    if code =='BCH':
        return 'USDC_'+code+'ABC'
    else:
        return 'USDT_'+code

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)

    url = "https://poloniex.com/public?command=returnTicker"
    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get symbol from poloniex')
    if response is None:
        return None
    data = {}
    data['source'] = 'poloniex'
    try:
        data['bid'] = response.json()[symbol]['highestBid']
        data['ask'] = response.json()[symbol]['lowestAsk']   
        data['trade'] = response.json()[symbol]['last']
        print (data)
        return data
    except:
        return None
    
    
if __name__ == '__main__':              
    symbol = 'BCH'
    data = getUSDPrice(symbol)
    print(data)