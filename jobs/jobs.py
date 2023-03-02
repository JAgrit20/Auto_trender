from django.conf import settings
from django.shortcuts import render, get_object_or_404
from counter.models import Counter, Vwap_Telegram_data,PCR_data, PCR_data_past,BTC_Data
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
import pandas as pd
import datetime
import pandas_ta as ta
import sys, os
import math
from bs4 import BeautifulSoup



def clean_daily_db():
	print("Clean up")
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method

	# print(dtobj1)
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

	dtobj_india = dtobj3.astimezone(
		pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M")
	dtobj_indiaa = str(dtobj_india)

	if(dtobj_indiaa == "23:00" or dtobj_indiaa == "09:15"):
		print("running clean")
		PCR_data.objects.all().delete()


def Send_high():
	import requests
	import json

	url = "https://api.telegram.org/bot5820846301%3AAAHYbFAlHnqDfzbHFPZHdO1O1u6Y21UJzVg/sendMessage"

	payload = {
		"text": "Count is more than 40",
		"disable_web_page_preview": False,
		"disable_notification": False,
		"reply_to_message_id": None,
		"chat_id": "-1001691472772"
	}
	headers = {
		"accept": "application/json",
		"content-type": "application/json"
	}

	response = requests.post(url, json=payload, headers=headers)

	print(response.text)


# In[5]:
# Send_high()

def Send_low():
	import requests
	import json

	url = "https://api.telegram.org/bot5921643018:AAHmiFfQudRMNZNl3sG19zafMZD0OdfWGgA/sendMessage"

	payload = {
		"text": "Count is less than 10",
		"disable_web_page_preview": False,
		"disable_notification": False,
		"reply_to_message_id": None,
		"chat_id": "-1001691472772"
	}
	headers = {
		"accept": "application/json",
		"content-type": "application/json"
	}

	response = requests.post(url, json=payload, headers=headers)

	print(response.text)


def Telegram_data():
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
	if(count >= 4):
		# prev_spot = spot
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
		# spot = float(nifty_val)
		prev_spot = field_value_signal
		b = float(spot/100)
		b = float(b)
		c = math.floor(b)
		d = float((c+1 )*100)
		e = float((c-1 )*100)
		Telegram_data_entry = Vwap_Telegram_data(time=dtobj_indiaa,Nifty_strike=nifty_val,entry_price= e,exit_price=0,Count=count,type_of_option="CALL",net_point_captured=prev_spot-spot)
		# Send_low()
		ans = Telegram_data_entry.save()

def schedule_api():
	try:
		print("Schdule API")
		dtobj1 = datetime.datetime.utcnow()  # utcnow class method

		# print(dtobj1)
		dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

		# print(pytz.all_timezones) => To see all timezones
		dtobj_india = dtobj3.astimezone(
			pytz.timezone("Asia/Calcutta"))  # astimezone method
		print("India time data_add", dtobj_india)

		url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9'
		}
		response = requests.get(url, headers=headers).content
		data = json.loads(response.decode('utf-8'))

		expiry_dt = data['records']['expiryDates'][0]
		new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

		headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(new_url, headers=headers)
		dajs = json.loads(page.text)

		ce_values = [data['CE'] for data in dajs['records']['data']
					 if "CE" in data and data['expiryDate'] == expiry_dt]
		pe_values = [data['PE'] for data in dajs['records']['data']
					 if "PE" in data and data['expiryDate'] == expiry_dt]
		ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])

		pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])

		print(ce_dt.columns.tolist())

		totCE = ce_dt['openInterest'].sum()
		print("openInterest", totCE)
		tol_CE_vol = ce_dt['totalTradedVolume'].sum()
		print("totalTradedVolume", tol_CE_vol)
		totPE = pe_dt['openInterest'].sum()
		print("openInterest", totPE)
		tol_PE_vol = pe_dt['totalTradedVolume'].sum()
		print("totalTradedVolume", tol_PE_vol)

		# totCE = data['filtered']['CE']['totOI']
		totc = data['filtered']['CE']
		totp = data['filtered']['CE']
		# totPE = data['filtered']['PE']['totOI']
		# tol_PE_vol = data['filtered']['PE']['totVol']
		# tol_CE_vol = data['filtered']['CE']['totVol']
		nifty_val = 0
		nifty_val = data['filtered']['data'][0]['PE']['underlyingValue']
		dtobj_india = dtobj_india.strftime("%H:%M")
		dtobj_indiaa = str(dtobj_india)

		diff = tol_CE_vol - tol_PE_vol

		diffOI = totCE - totPE

		pcr = tol_PE_vol/tol_CE_vol
		pcrOI = totPE/totCE

		print("PCR", pcr)
		signal = "BUY"
		if(pcr > 1):
			signal = "BUY"
		else:
			signal = "SELL"

		pcr_data_entry = PCR_data(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol, pcrOI=pcrOI, diffOI=diffOI,
								  diff=diff, pcr=pcr, price=nifty_val, option_signal=signal, callOI=totCE, putOI=totPE)
		pcr_data_entry2 = PCR_data_past(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol, pcrOI=pcrOI, diffOI=diffOI,
										diff=diff, pcr=pcr, price=nifty_val, option_signal=signal, callOI=totCE, putOI=totPE)

		ans = pcr_data_entry.save()
		ans1 = pcr_data_entry2.save()
		print("saving data")
		# print("ans", ans)

	except Exception as e:
		print("something went wrong", e)

		# 77779

# def getting_btc_data_past():
# 	try:
# 		# print("getting_btc_data")
# 		dtobj1 = datetime.datetime.utcnow()  # utcnow class method

# 		# print(dtobj1)
# 		dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

# 		# print(pytz.all_timezones) => To see all timezones
# 		dtobj_india = dtobj3.astimezone(
# 			pytz.timezone("Asia/Calcutta"))  # astimezone method
# 		print("India time data_add", dtobj_india)

# 		url = 'https://api.taapi.io/rsi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjNiZGQyZjRmYzVhOGFkZmVjOWE4YmY2IiwiaWF0IjoxNjczMzg0NjkyLCJleHAiOjMzMTc3ODQ4NjkyfQ.EdXPuHkbcD1G024Pk9Ml0zTzhSfd2Ptbvueyor1Ifw0&exchange=binance&symbol=BTC/USDT&interval=1m'

# 		headers = {
# 			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
# 			'accept-encoding': 'gzip, deflate, br',
# 			# 'accept-language': 'en-US,en;q=0.9'
# 		}
# 		sma = 0
# 		response = requests.get(url, headers=headers).content
# 		data = json.loads(response.decode('utf-8'))
# 		# print("Data2",data)
# 		print("Data",data)
# 		rsi = float(data['value'])	

# 		dtobj_india = dtobj_india.strftime("%H:%M:%S")

# 		dtobj_indiaa = str(dtobj_india)
# # Add indicators, using data from before
# 		mydata = BTC_Data.objects.all().values()
# 		df = pd.DataFrame(list(BTC_Data.objects.all().order_by('id').values()))


# 		#Create a simple moving average with a 30 day window
# 		# SMA_30_pd = SMA_30_pd.DataFrame()('Adj Close').rolling(window=30).mean()

# 		df.ta.sma(close='RSI', length=7, append=True)


# 		# df.ta.sma(close='RSI', length=20, append=True)
		
# 		json_records = df.reset_index().to_json(orient ='records')
# 		data = []
# 		data = json.loads(json_records)
# 		# print("dfff",df)
# 		# print(df.tail(15))
# 		# print(df['SMA_7'].loc[df.index[-1]])
# 		sma =0


# 		field_name_signal = 'signal'
# 		field_name_price = 'price'

# 		obj = BTC_Data.objects.last()

# 		field_value_signal = getattr(obj, field_name_signal)
# 		field_value_price = getattr(obj, field_name_price)

# 		pcr_data_entry = BTC_Data(time=dtobj_indiaa, RSI=rsi,SMA=sma,price=field_value_price, signal=field_value_signal)

# 		ans = pcr_data_entry.save()
# 		print("saving data")
# 		# print("ans", ans)

# 	except Exception as e:
# 		exc_type, exc_obj, exc_tb = sys.exc_info()
# 		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# 		print(exc_type, fname, exc_tb.tb_lineno)
# 		print("something went wrong", e) 

		# 77779
def getting_btc_data():
	try:
		# print("getting_btc_data")
		dtobj1 = datetime.datetime.utcnow()  # utcnow class method

		# print(dtobj1)
		dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

		# print(pytz.all_timezones) => To see all timezones
		dtobj_india = dtobj3.astimezone(
			pytz.timezone("Asia/Calcutta"))  # astimezone method
		print("India time data_add", dtobj_india)

		# print("Data2",data)
		dtobj_india = dtobj_india.strftime("%H:%M:%S")

		dtobj_indiaa = str(dtobj_india)

		field_name_signal = 'signal'
		field_name_price = 'price'
		field_name_rsi = 'RSI'
		field_name_sma = 'SMA'
		field_name_adx = 'signal_adx'
		field_name_signal_5min= 'signal_5min'

		field_name_price_5min= 'price_5min'
		field_name_signal_adx_5min= 'signal_adx_5min'
		obj = BTC_Data.objects.last()
		# print("obj", obj)
		field_value_signal = getattr(obj, field_name_signal)
		field_value_price = getattr(obj, field_name_price)
		field_value_rsi = getattr(obj, field_name_rsi)
		field_value_sma = getattr(obj, field_name_sma)
		field_value_adx = getattr(obj, field_name_adx)
		field_value_5min = getattr(obj, field_name_signal_5min)
		field_value_5min_p = getattr(obj, field_name_price_5min)
		field_value_5min_adx = getattr(obj, field_name_signal_adx_5min)

		pcr_data_entry = BTC_Data(time=dtobj_indiaa, RSI=field_value_rsi,SMA=field_value_sma,price=field_value_price, signal=field_value_signal,signal_adx = field_value_adx,signal_5min = field_value_5min,price_5min=field_value_5min_p,signal_adx_5min=field_value_5min_adx)

		ans = pcr_data_entry.save()
		print("saving data")
		# print("ans", ans)

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print("something went wrong", e) 

		# 77779
