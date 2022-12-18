import json
import requests
import pandas as pd

def getCurrentPCR(symbol):
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+symbol
    headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers).content
    data = json.loads(response.decode('utf-8'))
    # print(data)
    totCE = data['filtered']['CE']
    totc = data['filtered']['CE']
    totp = data['filtered']['CE']
    totPE = data['filtered']['PE']['totOI']

    print("totCE",totc)
    # print("totPE",totp)
    
    # print(totPE/totCE)
    return True


pcr = getCurrentPCR('NIFTY')

print('PCR = ', pcr)        