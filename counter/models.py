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
    callOI = models.BigIntegerField() 
    putOI = models.BigIntegerField() 
    diffOI = models.BigIntegerField() 
    diff = models.BigIntegerField() 
    pcr = models.FloatField() 
    pcrOI = models.FloatField() 
    option_signal = models.CharField(max_length=10) 
    price = models.BigIntegerField() 
class PCR_data_past(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    call = models.BigIntegerField() 
    put = models.BigIntegerField() 
    callOI = models.BigIntegerField(blank=True,null=True) 
    putOI = models.BigIntegerField(blank=True,null=True) 
    diffOI = models.BigIntegerField(blank=True,null=True) 
    diff = models.BigIntegerField() 
    pcr = models.FloatField() 
    pcrOI = models.FloatField() 
    option_signal = models.CharField(max_length=10) 
    price = models.BigIntegerField() 
