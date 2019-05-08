
# coding: utf-8

# In[1]:


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

    symbol_list = util.requestTimeout(url='https://api.btcmarkets.net/v2/market/active',timeout =waittime,errMsg='cannot get symbol in BTCMarkets')
    if symbol_list == None:
        return None

    for i in symbol_list.json()['markets']:
        symbol = i['instrument']
        if code == symbol:
            return symbol        
    return None

def getUSDPrice(symbol):
    symbol = getSymbol(symbol)
    if symbol == None:
        return None

    url = "https://api.btcmarkets.net/market/%s/AUD/tick"%symbol
    response = util.requestTimeout(url=url,timeout=waittime,errMsg='cannot get market data in BTCMarkets')
    if response is None:
        return None
    data = {}
    data['source'] = 'BTCMarkets'
    data['bid'] = response.json()['bestBid']
    data['ask'] = response.json()['bestAsk']
    data['trade'] = response.json()['lastPrice']
    
    response = util.requestTimeout(url='http://free.currencyconverterapi.com/api/v5/convert?q=AUD_USD&compact=y',timeout =0.1)
    if response is not None:
        exchange_rate = float(response.json()['AUD_USD']['val'])
    else:
        response = util.requestTimeout(url='https://api.exchangeratesapi.io/latest?base=AUD',timeout=0.1)
        if response is not None:
            exchange_rate = response.json()['rates']['USD']
        else:
            exchange_rate = 0.70
    data['bid'] = round(float(data['bid'])*exchange_rate,4)
    data['ask'] = round(float(data['ask'])*exchange_rate,4)
    data['trade'] = round(float(data['trade'])*exchange_rate,4)
    print(data)
    return data
    
if __name__ == '__main__':              
    symbol = 'ETC'
    data = getUSDPrice(symbol)
    print(data)



