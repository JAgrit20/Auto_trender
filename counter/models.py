from django.db import models
import datetime

class Counter(models.Model):
    key = models.CharField(max_length=10)
    value = models.IntegerField() 
class PCR_data(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    call = models.BigIntegerField() 
    put = models.BigIntegerField() 
    diff = models.BigIntegerField() 
    pcr = models.FloatField() 
    option_signal = models.CharField(max_length=10) 
    price = models.BigIntegerField() 
class PCR_data_past(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    call = models.BigIntegerField() 
    put = models.BigIntegerField() 
    diff = models.BigIntegerField() 
    pcr = models.FloatField() 
    option_signal = models.CharField(max_length=10) 
    price = models.BigIntegerField() 
