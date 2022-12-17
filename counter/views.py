from django.shortcuts import render, get_object_or_404
from .models import Counter, PCR_data
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

    context = {'mydata':mydata}
    return render(request, 'counter/index.html', context)


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

    totCE = data['filtered']['CE']['totOI']
    totc = data['filtered']['CE']
    totp = data['filtered']['CE']
    totPE = data['filtered']['PE']['totOI']
    tol_PE_vol = data['filtered']['PE']['totVol']
    tol_CE_vol = data['filtered']['CE']['totVol']
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
