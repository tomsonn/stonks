#!/usr/bin/env python3

import click
import json

from classes.binance import Binance
from classes.candlestick import Candlestick
from classes.exceptions import NotEnoughArguments
from utils.utils import write_to_file, assemble_file_path

from pprint import pprint as pp


FILE_PATH_HAMMER = './data/hammer_values/'

@click.command()
@click.option('--update', '-u', default='USDT', help='Update file with all coinpairs accessible on Binance.')
@click.option('--hammer', '-h', help='Get hammer candle in specific time range')
def main(update, hammer):
    bot = Binance()

    time_range = 8

    base_coin = update or 'USDT'
    interval = hammer or '15m'

    _file_path_hammer = assemble_file_path(FILE_PATH_HAMMER, interval)

    coin_pairs = bot.get_coin_pairs(base_coin)
    for coin_pair in coin_pairs:
        print(f'Analyzing {coin_pair} coin pair...')

        try:
            kline_data = bot.get_candlestick_data(symbol=coin_pair, interval=interval)
        except NotEnoughArguments as e:
            print(e)

        candles = [Candlestick(candlestick_idx, data, interval) for candlestick_idx, data in enumerate(kline_data)]

        print(f'COIN PAIR: {coin_pair}')
        for c in candles:
            res = c.get_resistance_area(candles)
            supp = c.get_support_area(candles)

            if supp:
                print('\nSUPPORT')
                pp(c.get_data())

            if res:
                print('\nRESISTANCE')
                pp(c.get_data())

        exit()

        hammers = {}
        for candle in candles:
            try:
                if candle.is_hammer() and candle.is_in_timerange(time_range):
                    if not hammers.get(coin_pair):
                        hammers[coin_pair] = []

                    hammers[coin_pair].append(candle.get_data())
            except ZeroDivisionError:
                print(f'ZeroDivisionError for coin pair: {coin_pair}')
                pp(candle.get_data())

        if hammers:
            was_writing_successful = write_to_file(json.dumps(hammers, indent=4), _file_path_hammer)
            print(f'Writing into file {_file_path_hammer} was successful.'
                  if was_writing_successful else
                  f'Something went wrong while writing into file {_file_path_hammer}.')
        else:
            print(f'For coin pair {coin_pair} hammer was not found.')


if __name__ == '__main__':
    main()
