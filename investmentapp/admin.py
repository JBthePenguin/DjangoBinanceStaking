from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from investmentapp.models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('invest_date', 'coin', 'amount', 'usd_amount')
    list_filter = ('invest_date', ('coin', AllValuesFieldListFilter))
