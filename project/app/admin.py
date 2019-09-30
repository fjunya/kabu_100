from django.contrib import admin
from .models import *

class RawPricesAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume', 'adjustment_close_price')

admin.site.register(Company)
admin.site.register(RawPrices, RawPricesAdmin)