from django.contrib import admin

from counter.models import PCR_data,PCR_data_past

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)
class RatingAdmin2(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(PCR_data,RatingAdmin)
admin.site.register(PCR_data_past,RatingAdmin2)
# Register your models here.
