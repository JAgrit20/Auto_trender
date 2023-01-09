from rest_framework import serializers
from .models import BTC_Data
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BTC_Data
        fields = ["time", "RSI", "SMA"]