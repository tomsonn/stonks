#!/usr/bin/env python3

from classes.binance import Binance
from classes.candlestick import Candlestick

from pprint import pprint as pp
from classes.exceptions import NotEnoughArguments


def main():
    BASE_COIN = 'USDT'

    bot = Binance()

    # coin_pairs = bot.get_coin_pairs(BASE_COIN)
    # pp(coin_pairs)

    symbol = 'BTC' + BASE_COIN
    interval = '5m'
    try:
        kline_data = bot.get_candlestick_data(symbol=symbol, interval=interval)
        # pp(kline_data)
    except NotEnoughArguments as e:
        print(e)

    candles = [Candlestick(data) for data in kline_data]
    hammers = [candle.get_data() for candle in candles if candle.is_hammer()]

    pp(hammers)


if __name__ == '__main__':
    main()
