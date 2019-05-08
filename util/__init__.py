import requests

def requestTimeout(url,timeout,errMsg='',payload=None):
    try:
        if payload ==None:
            req = requests.get(url,timeout=timeout)
        else:
            req = requests.get(url,params=payload,timeout=timeout)
    except:
        print(errMsg)
        return None
    if req.status_code is not 200:
        return None
    return req