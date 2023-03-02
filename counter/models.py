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
class Vwap_Telegram_data(models.Model):

    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    Count = models.BigIntegerField()
    Nifty_strike = models.FloatField()
    entry_price = models.FloatField()
    exit_price = models.FloatField()
    type_of_option =models.CharField(max_length=10)
    net_point_captured = models.FloatField()




class Telegram_data_past(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    Nifty_prev = models.FloatField()
    Nifty_new = models.FloatField()
    Count = models.BigIntegerField()
    RSI = models.FloatField()
    Color_code = models.CharField(max_length=10)
    final_signal = models.CharField(max_length=10)
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
class BTC_Data(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    RSI = models.FloatField()
    SMA = models.FloatField(blank=True)
    Analysis = models.TextField(blank=True)
    signal = models.BigIntegerField(blank=True,null=True)
    signal_5min = models.BigIntegerField(blank=True,null=True)
    signal_adx = models.BigIntegerField(blank=True,null=True)
    signal_adx_5min = models.BigIntegerField(blank=True,null=True)
    price_5min = models.BigIntegerField(blank=True,null=True)
    price = models.BigIntegerField(blank=True)
class Stocastic_Data(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    Stocastic_up = models.FloatField(blank=True)
    Stocastic_down = models.FloatField(blank=True)
    ADX = models.FloatField(blank=True,null= True)
    Final_call = models.FloatField(blank=True ,null= True)
    
class Stocastic_Data_DXY(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    Stocastic_up = models.FloatField(blank=True)
    Stocastic_down = models.FloatField(blank=True)
    ADX = models.FloatField(blank=True,null= True)
    Final_call = models.FloatField(blank=True ,null= True)
    


class Nifty_Data(models.Model):

    date = models.DateTimeField(auto_now_add=True, blank=True)
    entry_time = models.CharField(max_length=10)
    Nifty_entry = models.FloatField()
    Nifty_exit = models.FloatField(blank=True)
    exit_time = models.CharField(blank=True,max_length=10)
    move = models.BigIntegerField(blank=True,null=True)
    call_put = models.CharField(max_length=10,blank=True,null=True)
    Event_type = models.CharField(max_length=10,blank=True,null=True)
