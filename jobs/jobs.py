from django.conf import settings
from django.shortcuts import render, get_object_or_404
from counter.models import Counter, PCR_data,PCR_data_past
from django.http import HttpResponse
import json
import requests
import pandas as pd
from django.template import loader
import datetime as dt
import datetime
import pytz
import schedule
import time

def clean_daily_db():
		print("Clean up")
		dtobj1=datetime.datetime.utcnow()   #utcnow class method

		# print(dtobj1)
		dtobj3=dtobj1.replace(tzinfo=pytz.UTC) #replace method

		dtobj_india=dtobj3.astimezone(pytz.timezone("Asia/Calcutta")) #astimezone method
		print("India time",dtobj_india)
		dtobj_india = dtobj_india.strftime("%H:%M")
		dtobj_indiaa = str(dtobj_india)

		if(dtobj_indiaa == "23:00" or dtobj_indiaa == "09:15" ): 	
			print("running clean")
			PCR_data.objects.all().delete()	

def schedule_api():
	try:
		print("Schdule API")
		dtobj1=datetime.datetime.utcnow()   #utcnow class method

		# print(dtobj1)
		dtobj3=dtobj1.replace(tzinfo=pytz.UTC) #replace method


		#print(pytz.all_timezones) => To see all timezones
		dtobj_india=dtobj3.astimezone(pytz.timezone("Asia/Calcutta")) #astimezone method
		print("India time data_add",dtobj_india)



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

		print("PCR",pcr)
		signal = "BUY"
		if(pcr > 1):
			signal = "BUY"
		else:
			signal = "SELL"
		pcr_data_entry = PCR_data(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol,
								diff=diff, pcr=pcr, price=nifty_val, option_signal=signal)
		pcr_data_entry2 = PCR_data_past(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol,
								diff=diff, pcr=pcr, price=nifty_val, option_signal=signal)

		ans = pcr_data_entry.save()
		ans1 = pcr_data_entry2.save()
		print("saving data")
		# print("ans", ans)

	except Exception as e:
		print("something went wrong",e)

		#77779