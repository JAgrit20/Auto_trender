from django.contrib import admin

from counter.models import PCR_data

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)

admin.site.register(PCR_data,RatingAdmin)
# Register your models here.
