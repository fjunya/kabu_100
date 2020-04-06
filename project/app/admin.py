from django.contrib import admin
from .models import *

class RawPricesAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume', 'adjustment_close_price')

class ProfitAndLossAdmin(admin.ModelAdmin):
    list_display = ('code', 'average_buy_price', 'average_sell_price')

admin.site.register(Company)
admin.site.register(RawPrices, RawPricesAdmin)
admin.site.register(InvestmentRecord)
admin.site.register(ProfitAndLoss, ProfitAndLossAdmin)