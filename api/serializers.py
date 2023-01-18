from rest_framework import serializers
from .models import Task
from counter.models import Nifty_Data

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields ='__all__'
class Nifty_DataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Nifty_Data
		fields ='__all__'