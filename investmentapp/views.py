from django.shortcuts import render
from investmentapp.models import Investment, client
from stakingapp.models import Subscription, Redemption, FixedSaving


def index(request):
    # spot balances
    spot_balances = client.get_account()["balances"]
    # flexible savings
    flex_savings = client.get_lending_position()
    # prices
    prices = client.get_all_tickers()
    # coins datas
    coins = sorted(list(set(
        Investment.objects.all().values_list('coin', flat=True))))
    coins_datas = []
    total_coin_usd_interest = 0
    total_buy_invest_usd = 0
    total_present_invest_usd = 0
    for coin in coins:
        # staking amount
        staking_coin_amount = round(sum(
            Subscription.objects.filter(coin=coin).values_list('amount', flat=True)) - sum(
                Redemption.objects.filter(coin=coin).values_list('amount', flat=True)), 8)
        # fixed saving amount
        fixed_saving_coin_amount = round(sum(
            FixedSaving.objects.filter(coin=coin).values_list('amount', flat=True)), 8)
        # flexible saving amount
        try:
            flex_saving_amount = round(float(
                next((item for item in flex_savings if item["asset"] == coin), None)["freeAmount"]), 8)
        except TypeError:
            flex_saving_amount = 0
        # spot balance
        spot_balance = round(float(
            next((item for item in spot_balances if item["asset"] == coin), None)["free"]), 8)
        # invest coin amount
        invest_coin_amount = round(sum(
            Investment.objects.filter(coin=coin).values_list(
                'amount', flat=True)), 8)
        # present coin amount 
        present_coin_amount = round(
            staking_coin_amount + fixed_saving_coin_amount + spot_balance + flex_saving_amount, 8)
        # interest coin amount
        interest_coin_amount = round(
            present_coin_amount - invest_coin_amount, 8)
        # last price
        last_price_usd = round(float(
            next(
                (item for item in prices if item["symbol"] == f"{coin}USDT"),
                None)["price"]), 4)
        # interest coin amount in usd
        interest_coin_usd_amount = round(
            interest_coin_amount * last_price_usd, 2)
        # invest usd amount
        buy_invest_usd_amount = round(sum(
            Investment.objects.filter(coin=coin).values_list(
                'usd_amount', flat=True)), 2)
        # buy price
        buy_price_usd = round(buy_invest_usd_amount / invest_coin_amount, 4)
        # present usd amount
        present_invest_usd_amount = round(
            invest_coin_amount * last_price_usd, 2)
        # profit usd amount
        profit_usd_amount = round(
            present_invest_usd_amount - buy_invest_usd_amount, 2)
        # percent profit usd
        percent_profit_usd = round(
            profit_usd_amount * 100 / buy_invest_usd_amount, 2)
        # datas
        datas = {
            'invest_coin_amount': invest_coin_amount,
            'present_coin_amount': present_coin_amount,
            'interest_coin_amount': interest_coin_amount,
            'interest_coin_usd_amount': interest_coin_usd_amount,
            'buy_price_usd': buy_price_usd,
            'last_price_usd': last_price_usd,
            'buy_invest_usd_amount': buy_invest_usd_amount,
            'present_invest_usd_amount': present_invest_usd_amount,
            'profit_usd_amount': profit_usd_amount,
            'percent_profit_usd': percent_profit_usd,            
        }
        coins_datas.append((coin, datas))
        total_coin_usd_interest += interest_coin_usd_amount
        total_buy_invest_usd += buy_invest_usd_amount
        total_present_invest_usd += present_invest_usd_amount
    # total
    total = {
        'coin_usd_interest': round(total_coin_usd_interest, 2),
        'buy_invest_usd': round(total_buy_invest_usd, 2),
        'present_invest_usd': round(total_present_invest_usd, 2),
        'profit_usd': round(total_present_invest_usd - total_buy_invest_usd, 2),
    }
    total['percent_profit_usd'] = round(
            total['profit_usd'] * 100 / total_buy_invest_usd, 2)
    context = {
        'coins_datas': coins_datas,
        'total': total
    }
    return render(request, 'investmentapp/index.html', context)
