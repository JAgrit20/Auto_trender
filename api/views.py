from django.shortcuts import render
from django.http import JsonResponse
from counter.models import Counter, PCR_data, PCR_data_past,BTC_Data
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,Nifty_DataSerializer
import datetime as dt
import datetime
import pytz
import schedule
import time

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
	
	field_name_signal = 'signal'
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):
		objs.signal = 1
		objs.save()
		print("Updated BUY (1) success")
	if(request.data['title']=="SELL"):
		objs.signal = 0
		objs.save()
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

	serializer = Nifty_DataSerializer(data=request.data)
	# spot = float(request.data['entry'] )
	# b = spot/100
	# c = floor(b)
	# d = (c+1 )*100
	# e = (c-1 )*100


	if serializer.is_valid():
		serializer.save(
		# move=d,
		)
	else:
		print("Data not saved")

	return Response(serializer.data)
@api_view(['POST'])
def Nifty_Create_exit(request):

	serializer = Nifty_DataSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	else:
		print("Data not saved")

	return Response(serializer.data)

@api_view(['POST'])
def taskCreate_ADX(request):
	
	field_name_signal = 'signal_adx'
	objs = BTC_Data.objects.last()
	print("request.data",request.data)
	if(request.data['title']=="BUY"):

		objs.signal_adx = 1
		objs.save()
		print("Updated BUY (1) success")
	if(request.data['title']=="SELL"):
		objs.signal_adx = 0
		objs.save()
		print("Updated SELL (0) success")
	serializer = TaskSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

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



