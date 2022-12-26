from django.shortcuts import render, get_object_or_404
from .models import Counter, PCR_data,Telegram_data
from django.http import HttpResponse
import json
import requests
import pandas as pd
from django.template import loader
import datetime as dt
import datetime
import pytz
import time

def index(request):



    mydata = PCR_data.objects.all().values()
    # url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    # headers = {
    # 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    # 'accept-encoding' : 'gzip, deflate, br',
    # 'accept-language' : 'en-US,en;q=0.9'
    # }
    # response = requests.get(url, headers=headers).content
    #
    # data = json.loads(response.decode('utf-8'))
    # nifty_exp_date = data['records']['expiryDates']
    # if(request.GET):
    #     print("Get dat",(request.GET['expiry']))
    #     ind = int(request.GET['expiry'])
    #     selected_exp =  data['records']['expiryDates'][ind-1]
    #
    # else:
    #     selected_exp =  data['records']['expiryDates'][0]
    #     print("running else" )
    #
    # print("nif",nifty_exp_date)

    context = {'mydata':mydata   }


    return render(request, 'counter/index.html', context)

def strategy_2(request):

    mydata = Telegram_data.objects.all().values()
    context = {'mydata':mydata   }


    return render(request, 'counter/15min_ind.html', context)

def save_data(symbol):

    dtobj1=datetime.datetime.utcnow()   #utcnow class method
    print(dtobj1)

    dtobj3=dtobj1.replace(tzinfo=pytz.UTC) #replace method



    #print(pytz.all_timezones) => To see all timezones
    dtobj_india=dtobj3.astimezone(pytz.timezone("Asia/Calcutta")) #astimezone method
    print(dtobj_india)



    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers).content
    data = json.loads(response.decode('utf-8'))
    expiry_dt =  data['records']['expiryDates'][0]

    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])


    # print(ce_dt)
    print(ce_dt.columns.tolist())

    Total = ce_dt['openInterest'].sum()
    print("openInterest",Total)
    tol_CE_vol = ce_dt['totalTradedVolume'].sum()
    print("totalTradedVolume",tol_PE_vol)

    Total3 = pe_dt['openInterest'].sum()
    print("openInterest",Total3)
    tol_PE_vol = pe_dt['totalTradedVolume'].sum()
    print("totalTradedVolume",tol_PE_vol)

    totCE = data['filtered']['CE']['totOI']
    totc = data['filtered']['CE']
    totp = data['filtered']['CE']
    totPE = data['filtered']['PE']['totOI']
    # tol_PE_vol = data['filtered']['PE']['totVol']
    # tol_CE_vol = data['filtered']['CE']['totVol']
    nifty_val = 0
    nifty_val = data['filtered']['data'][0]['PE']['underlyingValue']
    dtobj_india = dtobj_india.strftime("%H:%M")
    dtobj_indiaa = str(dtobj_india)

    diff = tol_CE_vol - tol_PE_vol

    pcr = tol_PE_vol/tol_CE_vol

    signal = "BUY"
    if(pcr > 1):
        signal = "BUY"
    else:
        signal = "SELL"
    pcr_data_entry = PCR_data(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol,
                              diff=diff, pcr=pcr, price=nifty_val, option_signal=signal)

    ans = pcr_data_entry.save()
    print("ans", ans)

    return HttpResponse("done")

def fetch_oi(expiry_dt):
    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])

    # print(ce_dt)
    print(ce_dt.columns.tolist())

    Total = ce_dt['openInterest'].sum()
    print("openInterest",Total)
    Total2 = ce_dt['totalTradedVolume'].sum()
    print("totalTradedVolume",Total2)

    Total3 = pe_dt['openInterest'].sum()
    print("openInterest",Total3)
    Total4 = pe_dt['totalTradedVolume'].sum()
    print("totalTradedVolume",Total4)

# @app.task
# def check_shut_down():
#     if not job():
#         # add task that'll run again after 2 secs
#         check_shut_down.delay((), countdown=3)
#     else:
#         # task completed; do something to notify yourself
#         return True

# def job():

#     print("I'm working...")

# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc):
#     print("Doing stuff...")
#     # do your stuff
#     sc.enter(6, 1, do_something, (sc,))

# s.enter(6, 1, do_something, (s,))
# s.run()

# schedule.every(1).seconds.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
