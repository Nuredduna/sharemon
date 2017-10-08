#!/usr/bin/env python3

# Documentation at https://pypi.python.org/pypi/yahoo-finance

from yahoo_finance import Share
share_apple = Share("AAPL")
print(share_apple.get_name())
print(share_apple.get_price())
print(share_apple.get_trade_datetime())
print(share_apple.get_currency())
print(share_apple.get_200day_moving_avg())
share_apple.refresh()
print(share_apple.get_price())

print("---")

from yahoo_finance import Currency
btc_in_eur = Currency("BTCEUR")
print(btc_in_eur.get_rate())
print(btc_in_eur.get_trade_datetime())
btc_in_eur.refresh()
print(btc_in_eur.get_rate())






