from django.db import models
from investmentapp.models import coin_choices


class Subscription(models.Model):
    subscription_date = models.DateTimeField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    lock_period = models.IntegerField(verbose_name='période en jours')
    end_date = models.DateField(verbose_name='date de fin')
    
    class Meta:
        ordering = ('-subscription_date', )
        unique_together = ('subscription_date', 'coin',)


class Redemption(models.Model):
    redemption_date = models.DateTimeField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    
    class Meta:
        ordering = ('-redemption_date', )
        unique_together = ('redemption_date', 'coin',)


class FixedSaving(models.Model):
    subscription_date = models.DateField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    lock_period = models.IntegerField(verbose_name='période en jours')
    end_date = models.DateField(verbose_name='date de fin')
    
    class Meta:
        ordering = ('-subscription_date', )


class InterestEarned(models.Model):
    earn_date = models.DateField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    usd_amount = models.FloatField(verbose_name='montant en $')
    
    class Meta:
        ordering = ('-earn_date', )
