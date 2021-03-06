from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from investmentapp.models import Investment, Reinvestment, ProfitEarned


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('invest_date', 'coin', 'amount', 'usd_amount')
    list_filter = ('invest_date', ('coin', AllValuesFieldListFilter))


@admin.register(Reinvestment)
class ReinvestmentAdmin(admin.ModelAdmin):
    list_display = ('reinvest_date', 'coin', 'amount')
    list_filter = ('reinvest_date', ('coin', AllValuesFieldListFilter))


@admin.register(ProfitEarned)
class ProfitEarnedAdmin(admin.ModelAdmin):
    list_display = ('earn_date', 'coin', 'amount', 'usd_amount')
    list_filter = ('earn_date', ('coin', AllValuesFieldListFilter))
