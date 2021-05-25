#!/usr/bin/env python3

from classes.binance import Binance

from pprint import pprint as pp


def main():
    BASE_COIN = 'USDT'

    bot = Binance()

    coin_pairs = bot.get_coin_pairs(BASE_COIN)
    pp(coin_pairs)

if __name__ == '__main__':
    main()
