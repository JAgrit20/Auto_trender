from django.shortcuts import render, get_object_or_404
from .models import Counter, PCR_data,BTC_Data,Nifty_Data,Vwap_Telegram_data,Stocastic_Data,Stocastic_Data_DXY
from django.http import HttpResponse
import json
import requests
import pandas as pd
from django.template import loader
import datetime as dt
import datetime
import pytz
import time
from django.db.models import Sum
import datetime
import math
from bs4 import BeautifulSoup



def Check_past(request):

	field_name = 'signal'
	obj = BTC_Data.objects.last()
	field_value_signal = getattr(obj, field_name)

	print("field_value_signal",field_value_signal)
	ans = field_value_signal

	return HttpResponse(json.dumps({'decision':ans}))
def Check(request):

	# mydata = BTC_Data.objects.last()
	# mydata_f = BTC_Data.objects.first()

	field_name = 'signal'
	field_name_2 = 'RSI'
	field_name_id = 'id'
	field_name_adx= 'signal_adx'
	field_name_signal_5min= 'signal_5min'
	field_name_signal_adx_5min= 'signal_adx_5min'

	obj = BTC_Data.objects.last()


	field_value_id = getattr(obj, field_name_id)
	# field_value_time = getattr(obj, field_name_time)
	field_value_signal = getattr(obj, field_name)
	# field_value_adx = getattr(obj, field_name_signal_adx)
	field_value_rsi = getattr(obj, field_name_2)
	# field_value_signal_adx = getattr(obj, field_name_signal_adx)
	field_value_adx = getattr(obj, field_name_adx)
	field_value_5min = getattr(obj, field_name_signal_5min)
	field_value_signal_adx_5min = getattr(obj, field_name_signal_adx_5min)

	# print("field_value_signal",field_value_signal)
	# print("field_value_rsi",field_value_rsi)
	# print("field_value_id",field_value_id)
	# print("field_value_adx",field_value_adx)

	# print("field_value_5min",field_value_5min)
	# print("field_value_adx_5min",field_value_signal_adx_5min)

	ans=2
	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans= 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price = ans)
	


	return HttpResponse(json.dumps({'decision':ans}))
def check_5min(request):

	# mydata = BTC_Data.objects.last()
	# mydata_f = BTC_Data.objects.first()

	field_name = 'signal'
	field_name_2 = 'RSI'
	field_name_id = 'id'
	field_name_adx= 'signal_adx'
	field_name_signal_5min= 'signal_5min'

	obj = BTC_Data.objects.last()


	field_value_id = getattr(obj, field_name_id)
	# field_value_time = getattr(obj, field_name_time)
	field_value_signal = getattr(obj, field_name)
	# field_value_adx = getattr(obj, field_name_signal_adx)
	field_value_rsi = getattr(obj, field_name_2)
	# field_value_signal_adx = getattr(obj, field_name_signal_adx)
	field_value_adx = getattr(obj, field_name_adx)
	field_value_5min = getattr(obj, field_name_signal_5min)

	# print("field_value_signal",field_value_signal)
	# print("field_value_rsi",field_value_rsi)
	# print("field_value_id",field_value_id)
	# print("field_value_adx",field_value_adx)
	# print("field_value_5min",field_value_5min)


	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0):
		ans = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	


	return HttpResponse(json.dumps({'decision':ans}))
def check_s3(request):

	obj = Stocastic_Data.objects.last()
	
	
	field_name = 'Stocastic_up'
	field_name_2 = 'Stocastic_down'
	field_name_id = 'id'
	field_name_adx = 'ADX'
	field_name_time = 'time'
	field_value_id = getattr(obj, field_name_id)
	field_value_up = getattr(obj, field_name)
	field_value_down= getattr(obj, field_name_2)
	field_value_adx= getattr(obj, field_name_adx)
	field_value_time= getattr(obj, field_name_time)

	# print("field_value_id",field_value_id)
	# print("field_value_up",field_value_up)
	# print("field_value_down",field_value_down)
	# print("field_value_adx",field_value_adx)
	# print("field_value_time",field_value_time)
	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_up == 1 and field_value_down == 0 and field_value_adx == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_up== 0 and field_value_down == 1 and field_value_adx == 1):
		ans = 0
		
	Stocastic_Data.objects.filter(id =field_value_id).update(Final_call = ans)



	return HttpResponse(json.dumps({'decision':ans,'time':field_value_time}))
def check_s4(request):

	obj = Stocastic_Data_DXY.objects.last()
	
	
	field_name = 'Stocastic_up'
	field_name_2 = 'Stocastic_down'
	field_name_id = 'id'
	field_name_adx = 'ADX'
	field_name_time = 'time'
	field_value_id = getattr(obj, field_name_id)
	field_value_up = getattr(obj, field_name)
	field_value_down= getattr(obj, field_name_2)
	field_value_adx= getattr(obj, field_name_adx)
	field_value_time= getattr(obj, field_name_time)

	# print("field_value_id",field_value_id)
	# print("field_value_up",field_value_up)
	# print("field_value_down",field_value_down)
	# print("field_value_adx",field_value_adx)
	# print("field_value_time",field_value_time)
	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_up == 1 and field_value_down == 0 and field_value_adx == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_up== 0 and field_value_down == 1 and field_value_adx == 1):
		ans = 0
		
	Stocastic_Data_DXY.objects.filter(id =field_value_id).update(Final_call = ans)
	return HttpResponse(json.dumps({'decision':ans,'time':field_value_time}))
def Check_both(request):

	# mydata = BTC_Data.objects.last()
	# mydata_f = BTC_Data.objects.first()

	field_name = 'signal'
	field_name_2 = 'RSI'
	field_name_id = 'id'
	field_name_adx= 'signal_adx'
	field_name_signal_5min= 'signal_5min'
	field_name_signal_adx_5min= 'signal_adx_5min'

	obj = BTC_Data.objects.last()


	field_value_id = getattr(obj, field_name_id)
	# field_value_time = getattr(obj, field_name_time)
	field_value_signal = getattr(obj, field_name)
	# field_value_adx = getattr(obj, field_name_signal_adx)
	field_value_rsi = getattr(obj, field_name_2)
	# field_value_signal_adx = getattr(obj, field_name_signal_adx)
	field_value_adx = getattr(obj, field_name_adx)
	field_value_5min = getattr(obj, field_name_signal_5min)
	field_value_signal_adx_5min = getattr(obj, field_name_signal_adx_5min)

	# print("field_value_signal",field_value_signal)
	# print("field_value_rsi",field_value_rsi)
	# print("field_value_id",field_value_id)
	# print("field_value_adx",field_value_adx)

	# print("field_value_5min",field_value_5min)
	# print("field_value_adx_5min",field_value_signal_adx_5min)

	# field_value_rsi = float(field_value_rsi)
	# field_value_sma = float(field_value_sma)

	# latest_second = BTC_Data.objects.filter().order_by('-pk')[1]
	# field_value_sma_2 = getattr(latest_second, field_name)
	# field_value_rsi_2 = getattr(latest_second, field_name_2)

	# print("field_value_sma_2",field_value_sma_2)
	# print("field_value_sma_2",field_value_sma_2)
	# field_value_rsi_2 = float(field_value_rsi_2)
	# field_value_sma_2 = float(field_value_sma_2)

	# 1 == buy
	# 0 == sell
	# 2 == null

	ans = 2
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 0
	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_signal_adx == 1 ):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_signal_adx ==0   ):
		ans = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price = ans)
	


	return HttpResponse(json.dumps({'decision':ans}))

def index(request):
	mydata = Nifty_Data.objects.all().values()

	today = datetime.date.today()

	result = Nifty_Data.objects.filter(date__contains=today).aggregate(Sum('move'))

	net_sum = result['move__sum']

	# Print the result
	# print("The net sum of the 'move' column for {} is: {}".format(today, net_sum))
	# print("The net sum of the 'move' column for {} is: {}".format(today, net_sum))

	context = {'mydata':mydata,'net_sum':net_sum}


	return render(request, 'counter/index.html', context)

def strategy_2(request):

	mydata = BTC_Data.objects.all()[:10]
	df = pd.DataFrame(list(BTC_Data.objects.all().order_by('id').values()))


	# df['SMA_10'] = df['RSI'].rolling(window=10).mean()
# print the first 15 rows of data
	# print(df.head(15))
	import pandas_ta as ta
# Add indicators, using data from before

	df.ta.sma(close='RSI', length=7, append=True)

	# df.ta.sma(close='RSI', length=20, append=True)
	# print(df)
	json_records = df.tail(3500).reset_index().to_json(orient ='records')      
	data = []
	data = json.loads(json_records)
	context = {'mydata':mydata, 'd':data }

	return render(request, 'counter/15min_ind.html', context)
def strategy_3(request):

	mydata = Stocastic_Data.objects.all()[:10]
	df = pd.DataFrame(list(Stocastic_Data.objects.all().order_by('id').values()))
	# print(df)
	json_records = df.tail(3500).reset_index().to_json(orient ='records')      
	data = []
	data = json.loads(json_records)
	context = {'mydata':mydata, 'd':data }

	return render(request, 'counter/Socastic.html', context)
def strategy_4(request):

	mydata = Stocastic_Data_DXY.objects.all()[:10]
	df = pd.DataFrame(list(Stocastic_Data_DXY.objects.all().order_by('id').values()))
	# print(df)
	json_records = df.tail(3500).reset_index().to_json(orient ='records')      
	data = []
	data = json.loads(json_records)
	context = {'mydata':mydata, 'd':data }

	return render(request, 'counter/Socastic_DXY.html', context)
def strategy_5(request):

	print("Running VWAP")

	print("Telegram_data add")
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	stockcode = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO',
				 'HINDUNILVR', 'HDFC', 'ICICIBANK', 'ITC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']
	# print(stockcode)
	url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9'
	}
	response = requests.get(url, headers=headers).content
	data = json.loads(response)
	count = 0
	nifty_val = 0
	nifty_val = data['filtered']['data'][0]['PE']['underlyingValue']
	print("nifty_val", nifty_val)

	for i in range(len(stockcode)):
			try:
				stock_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' + \
					str(stockcode[i])
				print(stock_url)
				headers = {
					'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
				response = requests.get(stock_url, headers=headers)
				# response
				soup = BeautifulSoup(response.text, 'html.parser')
				data_array = soup.find(id='responseDiv').getText()

				y = json.loads(data_array)

				latest_price = (y['data'][-1]['lastPrice'])
				latest_price = latest_price.replace(',', '')
				print("latest", latest_price)
				latest_price = float(latest_price)

				# name = "SUNPHARMA"

				url = f'https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={stockcode[i]}&smeFlag=0&itpFlag=0'
				headers = {
					'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

				soup = BeautifulSoup(requests.get(
					url, headers=headers).content, 'html.parser')
				data = json.loads(soup.select_one('#responseDiv').text)

				# uncomment this to print all data:
				# print(json.dumps(data, indent=4))
				vwap = (data['data'][0]['averagePrice'])
				vwap = vwap.replace(',', '')
				vwap = float(vwap)
				# print("v",type(vwap))
				# print("latest_price",type(latest_price))
				vwap = float(vwap)

				print('vwap:', data['data'][0]['averagePrice'])

				if(latest_price > vwap):
					count = count + 1
				# print("yes big")
				# else:
				#   # print("small")
			except Exception as e:
				print("ERROR : "+str(e))
	
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method
	dtobj_india = dtobj3.astimezone(pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time data_add", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M")
	dtobj_indiaa = str(dtobj_india)
	print("count", count)
	field_value_signal = 0
	try:
		field_name = 'Nifty_strike'
		obj = Vwap_Telegram_data.objects.last()
		field_value_signal = getattr(obj, field_name)
	except:
		pass
	if(count >= 40):
		
		prev_spot = field_value_signal
		spot = float(nifty_val)
		b = float(spot/100)
		b = float(b)
		c = math.floor(b)
		d = float((c+1 )*100)
		e = float((c-1 )*100)
		Telegram_data_entry = Vwap_Telegram_data(time=dtobj_indiaa,Nifty_strike=nifty_val,entry_price= d,exit_price=0,Count=count,type_of_option="PUT",net_point_captured=prev_spot-spot)
		# Send_high()
		ans = Telegram_data_entry.save()

	if(count <= 10):
		prev_spot = field_value_signal
		spot = float(nifty_val)
		b = float(spot/100)
		b = float(b)
		c = math.floor(b)
		d = float((c+1 )*100)
		e = float((c-1 )*100)
		Telegram_data_entry = Vwap_Telegram_data(time=dtobj_indiaa,Nifty_strike=nifty_val,entry_price= e,exit_price=0,Count=count,type_of_option="CALL",net_point_captured=prev_spot-spot)
		# Send_low()
		ans = Telegram_data_entry.save()

	mydata = Vwap_Telegram_data.objects.all()[:10]
	df = pd.DataFrame(list(Vwap_Telegram_data.objects.all().order_by('id').values()))
	# print(df)
	json_records = df.tail(3500).reset_index().to_json(orient ='records')      
	data = []
	data = json.loads(json_records)
	context = {'mydata':mydata, 'd':data }

	return render(request, 'counter/index_vwap.html', context)

def save_data(symbol):

	dtobj1=datetime.datetime.utcnow()   #utcnow class method
	# print(dtobj1)

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
