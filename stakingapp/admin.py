from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from django.urls import path
from django.http import HttpResponseRedirect
from django.db.utils import IntegrityError
import pandas as pd
import warnings
from stakingapp.models import Subscription, Redemption, FixedSaving
from stakingapp.forms import UploadFileForm


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    change_list_template = "stakingapp/subscription_changelist.html"
    list_display = (
        'subscription_date',
        'coin',
        'amount',
        'lock_period',
        'end_date',
    )
    list_filter = ('subscription_date', 'end_date', ('coin', AllValuesFieldListFilter))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_subscription/', self.update_subscription),
        ]
        return my_urls + urls

    def update_subscription(self, request):
        if request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                with warnings.catch_warnings(record=True):
                    warnings.simplefilter("always")
                    subscriptions_excel = pd.read_excel(request.FILES['file'], engine="openpyxl")
                    subscriptions = subscriptions_excel.to_dict('records')
                    for subscription in subscriptions:
                        lock_period=int(subscription['Lock Period'].split()[0])
                        subscription_date=subscription['Subscription Date(UTC)']
                        try:
                            Subscription.objects.create(
                                subscription_date=subscription_date,
                                coin=subscription['Coin'],
                                amount=subscription['Total Amount'],
                                lock_period=lock_period,
                                end_date=pd.to_datetime(subscription_date) + pd.DateOffset(days=lock_period + 2)
                            )
                        except IntegrityError:
                            pass
                self.message_user(request, "Les subscriptions ont été mises à jour")
        return HttpResponseRedirect("../")


@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    change_list_template = "stakingapp/redemption_changelist.html"
    list_display = (
        'redemption_date',
        'coin',
        'amount',
    )
    list_filter = ('redemption_date', ('coin', AllValuesFieldListFilter))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_redemption/', self.update_redemption),
        ]
        return my_urls + urls

    def update_redemption(self, request):
        if request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                with warnings.catch_warnings(record=True):
                    warnings.simplefilter("always")
                    redemptions_excel = pd.read_excel(request.FILES['file'], engine="openpyxl")
                    redemptions = redemptions_excel.to_dict('records')
                    for redemption in redemptions:
                        try:
                            Redemption.objects.create(
                                redemption_date=redemption['Redemption Date(UTC)'],
                                coin=redemption['Coin'],
                                amount=redemption['Redemption Amount'],
                            )
                        except IntegrityError:
                            pass
                self.message_user(request, "Les remboursements ont été mis à jour")
        return HttpResponseRedirect("../")


@admin.register(FixedSaving)
class FixedSavingAdmin(admin.ModelAdmin):
    list_display = (
        'subscription_date',
        'coin',
        'amount',
        'lock_period',
        'end_date',
    )
    list_filter = ('subscription_date', 'end_date', ('coin', AllValuesFieldListFilter))
