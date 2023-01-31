from django.shortcuts import render
from django.http import JsonResponse
from counter.models import Counter, PCR_data, PCR_data_past,BTC_Data,Nifty_Data
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,Nifty_DataSerializer
import datetime as dt
import datetime
import pytz
import schedule
import time
import math

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
	print("data",request.data)
	
	field_name_signal = 'signal'
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="buy"):
		# objs.signal = 1
		last_obj = BTC_Data.objects.last()
		last_obj.signal = 1
		last_obj.save()
		print("Updated BUY (1) success")
	if(request.data['title']=="sell"):
		last_obj = BTC_Data.objects.last()
		last_obj.signal = 0
		last_obj.save()
		print("Updated SELL (0) success")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
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
		print("Updated BUY (1) success")
	if(request.data['title']=="SELL"):
		last_obj = BTC_Data.objects.last()
		last_obj.RSI = 0
		last_obj.save()
		print("Updated SELL (0) success")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)


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
	if(request.data['title']=="buy"):
		try:

			nifty_data_entry = Nifty_Data(entry_time=dtobj_indiaa, Nifty_entry=e, Nifty_exit=0, exit_time=0 , move=0,call_put="CE")
			ans = nifty_data_entry.save()
		except Exception as e:
			print("something went while adding nifty", e)
	if(request.data['title']=="sell"):
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



