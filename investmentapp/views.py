from django.shortcuts import render
from investmentapp.models import Investment, Reinvestment, ProfitEarned ,client
from stakingapp.models import Subscription, Redemption, FixedSaving, InterestEarned


def index(request):
    # spot balances
    spot_balances = client.get_account()["balances"]
    # flexible savings
    flex_savings = client.get_lending_position()
    # prices
    prices = client.get_all_tickers()
    # init coins datas and totals
    coins = sorted(list(set(
        Investment.objects.all().values_list('coin', flat=True))))
    interests = []
    profits = []
    earns = []
    total_coin_usd_interest = 0
    total_buy_invest_usd = 0
    total_present_invest_usd = 0
    total_interest_earned = 0
    total_profit_earned = 0
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
        # available coin
        available = round(flex_saving_amount + spot_balance, 8)
        # invest coin amount
        invest_coin_amount = round(sum(
            Investment.objects.filter(coin=coin).values_list(
                'amount', flat=True)), 8) + round(sum(
                    Reinvestment.objects.filter(coin=coin).values_list(
                        'amount', flat=True)), 8) - round(sum(
                            ProfitEarned.objects.filter(coin=coin).values_list(
                                'amount', flat=True)), 8)
        # present coin amount 
        present_coin_amount = round(
            staking_coin_amount + fixed_saving_coin_amount + spot_balance + flex_saving_amount, 8)
        # interest coin amount
        interest_coin_amount = round(
            present_coin_amount - invest_coin_amount, 8)
        # percent interest coin
        percent_interest_coin = round(
            interest_coin_amount * 100 / invest_coin_amount, 2)
        # last price
        last_price_usd = round(float(
            next(
                (item for item in prices if item["symbol"] == f"{coin}USDT"),
                None)["price"]), 4)
        # interest coin amount in usd
        interest_coin_usd_amount = round(
            interest_coin_amount * last_price_usd, 2)
        # sell interest to earn
        sell_interest_to_earn = ""
        if interest_coin_usd_amount >= 15:
            coin_amount_to_sell = round(
                interest_coin_amount * 2 / 3, 8)
            if available >= coin_amount_to_sell:
                sell_interest_to_earn += f'sell {str(coin_amount_to_sell).replace(".", ",")}'
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
        # sell profit to earn
        sell_profit_to_earn = ""
        if percent_profit_usd >= 100:
            coin_amount_to_sell = round(
                (profit_usd_amount * 2 / 3) / last_price_usd, 8)
            if available >= coin_amount_to_sell:
                sell_profit_to_earn += f'sell {str(coin_amount_to_sell).replace(".", ",")}'
        # interest earned
        interest_earned = round(sum(
            InterestEarned.objects.filter(coin=coin).values_list(
                'usd_amount', flat=True)), 2)
        # profit earned
        profit_earned = round(sum(
            ProfitEarned.objects.filter(coin=coin).values_list(
                'usd_amount', flat=True)), 2)
        # total earned
        all_earned = round(interest_earned + profit_earned, 2)
        # datas
        interest_datas = {
            'invest_coin_amount': invest_coin_amount,
            'present_coin_amount': present_coin_amount,
            'percent_interest_coin': percent_interest_coin,
            'interest_coin_amount': interest_coin_amount,
            'interest_coin_usd_amount': interest_coin_usd_amount,
            'sell_interest_to_earn': sell_interest_to_earn
        }
        interests.append((coin, interest_datas))
        profit_datas = {            
            'buy_price_usd': buy_price_usd,
            'last_price_usd': last_price_usd,
            'buy_invest_usd_amount': buy_invest_usd_amount,
            'present_invest_usd_amount': present_invest_usd_amount,
            'profit_usd_amount': profit_usd_amount,
            'percent_profit_usd': percent_profit_usd,
            'sell_profit_to_earn': sell_profit_to_earn
        }
        profits.append((coin, profit_datas))
        if all_earned > 0:
            earn_datas = {
                'interest_earned': interest_earned,
                'profit_earned': profit_earned,
                'all_earned': all_earned,
                'percent_of_invest_earned': round(
                    all_earned * 100 / buy_invest_usd_amount, 2)
            }
            earns.append((coin, earn_datas))
        # totals
            total_interest_earned += interest_earned
            total_profit_earned += profit_earned
        total_coin_usd_interest += interest_coin_usd_amount
        total_buy_invest_usd += buy_invest_usd_amount
        total_present_invest_usd += present_invest_usd_amount
    # total
    total = {
        'coin_usd_interest': round(total_coin_usd_interest, 2),
        'buy_invest_usd': round(total_buy_invest_usd, 2),
        'present_invest_usd': round(total_present_invest_usd, 2),
        'profit_usd': round(total_present_invest_usd - total_buy_invest_usd, 2),
        'interest_earned': round(total_interest_earned, 2),
        'profit_earned': round(total_profit_earned, 2),
        
    }
    total['percent_profit_usd'] = round(
            total['profit_usd'] * 100 / total_buy_invest_usd, 2)
    total['all_earned'] = round(
            total['interest_earned'] + total['profit_earned'], 2)
    total['percent_of_invest_earned'] = round(
            total['all_earned'] * 100 / total_buy_invest_usd, 2)
    context = {
        "profits": profits,
        'interests': interests,
        "earns": earns,
        'total': total
    }
    return render(request, 'investmentapp/index.html', context)
