from django.shortcuts import render
from django.http import JsonResponse
from counter.models import Counter, PCR_data, PCR_data_past,BTC_Data,Nifty_Data,Stocastic_Data
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,Nifty_DataSerializer
import datetime as dt
import datetime
import pytz
import schedule
import time
import math
import json

from .models import Task
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):

	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.signal = 1
		last_obj.save()
		print("Updated BUY (1) success create")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.signal = 0
		last_obj.save()
		print("Updated SELL (0) success create")
	# serializer = TaskSerializer(data=request.data)
	# if serializer.is_valid():
	# 	serializer.save()
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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)
	print("field_value_5min",field_value_5min)
	print("field_value_adx_5min",field_value_signal_adx_5min)

	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1 and field_value_signal_adx_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0 and field_value_signal_adx_5min == 1):
		ans = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	
	return Response("Done")
@api_view(['POST'])
def taskCreate_data(request):

	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.signal = 1
		last_obj.save()
		print("Updated BUY (1) success create")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.signal = 0
		last_obj.save()
		print("Updated SELL (0) success create")
	# serializer = TaskSerializer(data=request.data)
	# if serializer.is_valid():
	# 	serializer.save()

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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)

	print("field_value_5min",field_value_5min)
	print("field_value_adx_5min",field_value_signal_adx_5min)

	ans = 2
	ans2 = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1 and field_value_signal_adx_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0 and field_value_signal_adx_5min == 1):
		ans = 0
	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	BTC_Data.objects.filter(id =field_value_id).update(price = ans2)
	return Response("Done")
	
@api_view(['POST'])
def taskCreate_data_5min(request):
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.signal_5min = 1
		last_obj.save()
		print("Updated BUY (1) success create")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.signal_5min = 0
		last_obj.save()
		print("Updated SELL (0) success create")

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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)

	print("field_value_5min",field_value_5min)
	print("field_value_adx_5min",field_value_signal_adx_5min)


	ans = 2
	ans2 = 2
	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1 and field_value_signal_adx_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0 and field_value_signal_adx_5min == 1):
		ans = 0
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	BTC_Data.objects.filter(id =field_value_id).update(price = ans2)
		
	return Response("Done")

@api_view(['POST'])
def taskCreate_adx(request):
	# print("data",request.data)
	# req_data = request.get_json(force=True)
	# print("json data",req_data)
	# request_body = request.data.decode('utf-8')	
	# data = json.loads(request_body)
	# print("json data",data)
	
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.signal_adx = 1
		last_obj.save()
		print("Updated BUY (1) success adx")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.signal_adx = 0
		last_obj.save()
		print("Updated SELL (0) success adx")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)

	print("field_value_5min",field_value_5min)
	print("field_value_adx_5min",field_value_signal_adx_5min)

	ans = 2
	ans2 = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1 and field_value_signal_adx_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0 and field_value_signal_adx_5min == 1):
		ans = 0
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	BTC_Data.objects.filter(id =field_value_id).update(price = ans2)		
	return Response(serializer.data)

@api_view(['POST'])
def taskCreate_RSI(request):
	
	field_name_signal = 'RSI'
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.RSI = 1
		last_obj.save()
		print("Updated BUY (1) success RSI")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.RSI = 0
		last_obj.save()
		print("Updated SELL (0) success RSI")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()

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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)

	print("field_value_5min",field_value_5min)
	print("field_value_adx_5min",field_value_signal_adx_5min)

	ans = 2
	ans2 = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1 and field_value_signal_adx_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0 and field_value_signal_adx_5min == 1):
		ans = 0
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	BTC_Data.objects.filter(id =field_value_id).update(price = ans2)	
	return Response(serializer.data)

@api_view(['POST'])
def taskCreate_ADX_5min(request):
	
	field_name_signal = 'RSI'
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.signal_adx_5min = 1
		last_obj.save()
		print("Updated BUY (1) success RSI")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.signal_adx_5min = 0
		last_obj.save()
		print("Updated SELL (0) success RSI")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)

	print("field_value_5min",field_value_5min)
	print("field_value_adx_5min",field_value_signal_adx_5min)

	ans = 2
	ans2 = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1 and field_value_signal_adx_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0 and field_value_signal_adx_5min == 1):
		ans = 0
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1  and field_value_signal_adx_5min == 1):
		ans2 = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)
	BTC_Data.objects.filter(id =field_value_id).update(price = ans2)	
	return Response(serializer.data)

@api_view(['POST'])
def taskCreate_data_stocastic_up(request):
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method
	dtobj_india = dtobj3.astimezone(
	pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M:%S")
	dtobj_indiaa = str(dtobj_india)
	Updated = "No"

	if(request.data['title']=="BUY"):
		pcr_data_entry = Stocastic_Data(time=dtobj_indiaa, Stocastic_up=1,Stocastic_down=0)
		ans = pcr_data_entry.save()
		Updated = "Buy Yes"
		print("Updated BUY (1) success stocastic")
	if(request.data['title']=="SELL"):
		pcr_data_entry = Stocastic_Data(time=dtobj_indiaa, Stocastic_up=0,Stocastic_down=1)
		ans = pcr_data_entry.save()
		Updated = "Sell No"
		print("Updated SELL (1) success stocastic")
	field_name = 'Stocastic_up'
	field_name_2 = 'Stocastic_down'
	field_name_id = 'id'
	field_name_adx = 'ADX'
	obj = Stocastic_Data.objects.last()

	field_value_id = getattr(obj, field_name_id)
	field_value_up = getattr(obj, field_name)
	field_value_down= getattr(obj, field_name_2)
	field_value_adx= getattr(obj, field_name_adx)

	print("field_value_id",field_value_id)
	print("field_value_up",field_value_up)
	print("field_value_down",field_value_down)
	print("field_value_adx",field_value_adx)

	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_up == 1 and field_value_down == 0 and field_value_adx == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_up== 0 and field_value_down == 1 and field_value_adx == 1):
		ans = 0
		
	Stocastic_Data.objects.filter(id =field_value_id).update(Final_call = ans)

	return Response(Updated)
@api_view(['POST'])
def taskCreate_data_stocastic_ADX(request):
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method
	dtobj_india = dtobj3.astimezone(
	pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M:%S")
	dtobj_indiaa = str(dtobj_india)
	Updated = "No"
	field_name = 'Stocastic_up'
	field_name_2 = 'Stocastic_down'
	field_name_id = 'id'
	field_name_adx = 'ADX'
	obj = Stocastic_Data.objects.last()
	
	field_value_id = getattr(obj, field_name_id)
	field_value_up = getattr(obj, field_name)
	field_value_down= getattr(obj, field_name_2)
	field_value_adx= getattr(obj, field_name_adx)

	print("field_value_id",field_value_id)
	print("field_value_up",field_value_up)
	print("field_value_down",field_value_down)
	print("field_value_adx",field_value_adx)

	if(request.data['title']=="BUY"):
		Stocastic_Data.objects.filter(id =field_value_id).update(ADX = 1)
		# pcr_data_entry = Stocastic_Data(time=dtobj_indiaa, Stocastic_up=1,Stocastic_down=0)
		# ans = pcr_data_entry.save()
		Updated = "Buy Yes"
		print("Updated BUY (1) success stocastic")
	if(request.data['title']=="SELL"):
		Stocastic_Data.objects.filter(id =field_value_id).update(ADX = 0)
		# pcr_data_entry = Stocastic_Data(time=dtobj_indiaa, Stocastic_up=0,Stocastic_down=1)
		# ans = pcr_data_entry.save()
		Updated = "Sell No"
		print("Updated SELL (1) success stocastic")
	obj = Stocastic_Data.objects.last()
	
	field_value_id = getattr(obj, field_name_id)
	field_value_up = getattr(obj, field_name)
	field_value_down= getattr(obj, field_name_2)
	field_value_adx= getattr(obj, field_name_adx)

	print("field_value_id",field_value_id)
	print("field_value_up",field_value_up)
	print("field_value_down",field_value_down)
	print("field_value_adx",field_value_adx)
	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_up == 1 and field_value_down == 0 and field_value_adx == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_up== 0 and field_value_down == 1 and field_value_adx == 1):
		ans = 0
		
	Stocastic_Data.objects.filter(id =field_value_id).update(Final_call = ans)

	return Response(Updated)


@api_view(['POST'])
def Nifty_Update(request):
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method

	# print(dtobj1)
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

	# print(pytz.all_timezones) => To see all timezones
	dtobj_india = dtobj3.astimezone(pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time data_add", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M:%S")

	dtobj_indiaa = str(dtobj_india)

	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	
	objs.Nifty_exit = request.data['exit']
	objs.exit_time = dtobj_indiaa
	objs.save()
	print("Updated exit success")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def Nifty_Create(request):
	data=request.data
	print("data_nifty",data)

	# serializer = Nifty_DataSerializer(data=request.data) 
	spot = float(request.data['entry'] )
	# b = spot/100
	# c = floor(b)
	# d = (c+1 )*100
	# e = (c-1 )*100
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	# print(dtobj1)
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

	dtobj_india = dtobj3.astimezone(
	pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M")
	dtobj_indiaa = str(dtobj_india)
	spot = float(spot)
	b = float(spot/100)
	b = float(b)

	c = math.floor(b)
	d = float((c+1 )*100)
	e = float((c-1 )*100)
	if(request.data['title']=="BUY"):
		try:

			nifty_data_entry = Nifty_Data(entry_time=dtobj_indiaa, Nifty_entry=e, Nifty_exit=0, exit_time=0 , move=0,call_put="CE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)
	if(request.data['title']=="SELL"):
		try:

			nifty_data_entry = Nifty_Data(entry_time=dtobj_indiaa, Nifty_entry=d, Nifty_exit=0, exit_time=0 , move=0,call_put="PE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)
	if(request.data['title']=="BUY_exit"):
		print("This is running")
		try:
			latest_row = Nifty_Data.objects.filter(call_put='CE').order_by('date').last()
			last_val = float( latest_row.Nifty_entry )
			last_val_time = ( latest_row.entry_time )
			last_val_timee = ( latest_row.Nifty_exit )
			print("last_val",last_val)
			print("spot",spot)
			move = float(spot - last_val)
			print("move",move) 

			nifty_data_entry = Nifty_Data(entry_time=last_val_time, Nifty_entry=last_val, Nifty_exit=spot, exit_time=dtobj_indiaa , move=move,call_put="CE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)
	if(request.data['title']=="SELL"):
		try:
			latest_row = Nifty_Data.objects.filter(call_put='PE').order_by('-date').last()
			last_val = float( latest_row.Nifty_entry )
			last_val_time = ( latest_row.entry_time )
			move = float(spot - last_val)

			nifty_data_entry = Nifty_Data(entry_time=last_val_time, Nifty_entry=last_val, Nifty_exit=spot, exit_time=dtobj_indiaa , move=move,call_put="PE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)
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

	print("field_value_signal",field_value_signal)
	print("field_value_rsi",field_value_rsi)
	print("field_value_id",field_value_id)
	print("field_value_adx",field_value_adx)
	print("field_value_5min",field_value_5min)


	ans = 2

	# if(field_value_rsi<=40 and (((field_value_rsi - field_value_rsi_2)>0  and field_value_rsi>= field_value_sma and field_value_sma>=field_value_rsi_2) or  field_value_sma <field_value_rsi ) and ((field_value_rsi <=60  ) or field_value_sma <field_value_rsi)   ):
	if(field_value_signal == 1 and field_value_rsi == 1 and field_value_adx == 1 and field_value_5min == 1):
		ans = 1
	# if (field_value_rsi >=60 and ((((field_value_rsi - field_value_rsi_2)<0  and (field_value_rsi_2>= field_value_sma and field_value_sma>=field_value_rsi) )) or field_value_sma > field_value_rsi ) and field_value_rsi >=37):
	if( field_value_signal== 0  and field_value_rsi == 0 and field_value_adx == 1 and field_value_5min == 0):
		ans = 0
		
	BTC_Data.objects.filter(id =field_value_id).update(price_5min = ans)

	return Response("Done")
@api_view(['POST'])
def Nifty_Create_exit(request):

	# serializer = Nifty_DataSerializer(data=request.data) 
	spot = float(request.data['exit'] )
	# b = spot/100
	# c = floor(b)
	# d = (c+1 )*100
	# e = (c-1 )*100
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	# print(dtobj1)
	dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

	dtobj_india = dtobj3.astimezone(
	pytz.timezone("Asia/Calcutta"))  # astimezone method
	print("India time", dtobj_india)
	dtobj_india = dtobj_india.strftime("%H:%M")
	dtobj_indiaa = str(dtobj_india)





	if(request.data['title']=="BUY_exit"):
		print("This is running")
		try:
			latest_row = Nifty_Data.objects.filter(call_put='CE').order_by('date').last()
			last_val = float( latest_row.Nifty_entry )
			last_val_time = ( latest_row.entry_time )
			last_val_timee = ( latest_row.Nifty_exit )
			print("last_val",last_val)
			print("spot",spot)
			move = float(spot - last_val)
			print("move",move) 

			nifty_data_entry = Nifty_Data(entry_time=last_val_time, Nifty_entry=last_val, Nifty_exit=spot, exit_time=dtobj_indiaa , move=move,call_put="CE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)
	if(request.data['title']=="SELL"):
		try:
			latest_row = Nifty_Data.objects.filter(call_put='PE').order_by('-date').last()
			last_val = float( latest_row.Nifty_entry )
			last_val_time = ( latest_row.entry_time )
			move = float(spot - last_val)

			nifty_data_entry = Nifty_Data(entry_time=last_val_time, Nifty_entry=last_val, Nifty_exit=spot, exit_time=dtobj_indiaa , move=move,call_put="PE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)

	return Response("Done")

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')



