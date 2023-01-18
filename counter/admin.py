from django.contrib import admin

from counter.models import PCR_data,PCR_data_past,BTC_Data,Nifty_Data

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)
class RatingAdmin2(admin.ModelAdmin):
    readonly_fields = ('date',)
class RatingAdmin3(admin.ModelAdmin):
    readonly_fields = ('date',)
class RatingAdmin4(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(PCR_data,RatingAdmin)
admin.site.register(PCR_data_past,RatingAdmin2)
admin.site.register(BTC_Data,RatingAdmin3)
admin.site.register(Nifty_Data,RatingAdmin4)
# Register your models here.
