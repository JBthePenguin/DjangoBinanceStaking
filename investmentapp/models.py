import datetime
# from sqlite3 import adapt
from django.db import models

# binance api doc
# Create your models here.
from binance.client import Client
from django.conf import settings

# settings.configure()

client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)

coins = sorted([c['coin'] for c in client.get_all_coins_info()])
# print(coins[0])
coin_choices = [(c, c) for c in coins]
# for coin_info in coins:
#     coin_choices.append((coin_info['coin'], coin_info['coin']))

class Investment(models.Model):
    invest_date = models.DateField(verbose_name='date')
    coin = models.CharField(choices=coin_choices, max_length=20, verbose_name='coin')
    amount = models.FloatField(verbose_name='montant')
    usd_amount = models.FloatField(verbose_name='total en $')
    
    class Meta:
        ordering = ('-invest_date', )



# amounts = []
# all_payments = client.get_fiat_payments_history(transactionType=0, beginTime=0)['data']
# for payment in all_payments:
#     if payment['status'] == 'Completed' and payment['cryptoCurrency'] == 'CAKE':
#         readable = datetime.datetime.fromtimestamp(payment['createTime'] / 1000)
#         print(readable)
#         print(payment['sourceAmount'])
#         amounts.append(float(payment['sourceAmount']))
#         print(payment)


# 2022-02-23 10:54:31
# 50.0
# {'orderNo': '5100360058614703989084cc7ceb3c4d', 'sourceAmount': '50.0', 'fiatCurrency': 'EUR', 'obtainAmount': '7.67638973', 'cryptoCurrency': 'CAKE', 'totalFee': '1.00', 'price': '6.383209', 'status': 'Completed', 'createTime': 1645613671000, 'updateTime': 1645613722000}
# 2022-02-07 09:41:11
# 50.0
# {'orderNo': 'N01187120995625543680020708', 'sourceAmount': '50.0', 'fiatCurrency': 'EUR', 'obtainAmount': '6.66156235', 'cryptoCurrency': 'CAKE', 'totalFee': '1.00', 'price': '7.35563182', 'status': 'Completed', 'createTime': 1644226871000, 'updateTime': 1644226928946}

# 2022-02-23  7.67638973 CAKE 56,7$
# 2022-02-07  6.66156235 CAKE 57.1$

# savings flexible
# flex_savings = client.get_lending_position()
# for saving in flex_savings:
#     print(saving)


# history
# flex_savings = client.get_lending_purchase_history(lendingType="DAILY")
# for saving in flex_savings:
#     print(saving)

# locked_savings = client.get_lending_purchase_history(lendingType="CUSTOMIZED_FIXED")
# for saving in locked_savings:
#     print(saving)

# locked_savings = client.get_fixed_activity_project_list(type="CUSTOMIZED_FIXED")
# for saving in locked_savings:
#     print(saving)




# print(client.get_lending_product_list())
# {'purchaseId': 1347616929, 'createTime': 1646986647000, 'productName': 'CAKE', 'asset': 'CAKE', 'amount': '0.66249022', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1347616207, 'createTime': 1646986193000, 'productName': 'CAKE', 'asset': 'CAKE', 'amount': '0.01', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1347597696, 'createTime': 1646979722000, 'productName': 'SAND', 'asset': 'SAND', 'amount': '0.00706764', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1347524553, 'createTime': 1646978856000, 'productName': 'MBOX', 'asset': 'MBOX', 'amount': '0.00549783', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1347509169, 'createTime': 1646978678000, 'productName': 'BTC', 'asset': 'BTC', 'amount': '0.00000027', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1347048620, 'createTime': 1646975811000, 'productName': 'BNB', 'asset': 'BNB', 'amount': '0.00000228', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1345128419, 'createTime': 1646948534000, 'productName': 'MBOX', 'asset': 'MBOX', 'amount': '0.00549775', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1345114340, 'createTime': 1646948371000, 'productName': 'BTC', 'asset': 'BTC', 'amount': '0.00000027', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1344347552, 'createTime': 1646945051000, 'productName': 'BNB', 'asset': 'BNB', 'amount': '0.00004505', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1339060773, 'createTime': 1646909686000, 'productName': 'USDT', 'asset': 'USDT', 'amount': '0.8104', 'status': 'SUCCESS', 'lendingType': 'DAILY'}
# {'purchaseId': 1953239, 'createTime': 1646986246000, 'productName': 'CAKE', 'asset': 'CAKE', 'lot': 4, 'amount': '4', 'status': 'SUCCESS', 'lendingType': 'CUSTOMIZED_FIXED'}