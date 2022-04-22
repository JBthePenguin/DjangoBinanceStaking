from django.db import models
from binance.client import Client
from django.conf import settings


client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)

coins = sorted([c['coin'] for c in client.get_all_coins_info()])
coin_choices = [(c, c) for c in coins]

class Investment(models.Model):
    invest_date = models.DateField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    usd_amount = models.FloatField(verbose_name='total en $')
    
    class Meta:
        ordering = ('-invest_date', )


class Reinvestment(models.Model):
    reinvest_date = models.DateField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    
    class Meta:
        ordering = ('-reinvest_date', )


class ProfitEarned(models.Model):
    earn_date = models.DateField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    usd_amount = models.FloatField(verbose_name='montant en $')
    
    class Meta:
        ordering = ('-earn_date', )
