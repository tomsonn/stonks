import os
import requests
import sys

from binance.client import Client
from datetime import datetime
from classes.exceptions import NotEnoughArguments


class Binance:

    def __init__(self):
        self.API_KEY = os.environ['BINANCE_API_KEY']
        self.API_SECRET = os.environ['BINANCE_API_SECRET']

        self.BASE_URL = 'https://api.binance.com'

        # Instance of Binance client
        self.client = Client(self.API_KEY, self.API_SECRET)

        # Dictionary ->
        # {
        #     'price': price [str],
        #     'symbol': coin_pair [str]
        # }
        self.coins_info = self.client.get_all_tickers()
        self.coins_file_path = 'data/coin_pairs.txt'

    def get_coin_pairs(self, base_currency: str = 'USDT') -> list:
        """Get all coin pairs for desired base currency"""

        if not self.is_file_updated(self.coins_file_path, 24):
            coin_pairs = [coin_data['symbol']
                          for coin_data in self.coins_info
                          if coin_data['symbol'][-len(base_currency):] == base_currency]

            with open(self.coins_file_path, 'w') as f:
                f.truncate(0)
                f.writelines([coin_pair + '\n' for coin_pair in coin_pairs])

            return coin_pairs
        else:
            with open(self.coins_file_path, 'r') as f:
                lines = f.readlines()

            return [line.strip() for line in lines]

    def get_candlestick_data(self, **params):
        """
            Return candlestick data as dict.
            If start_time and end_time are not passed as arguments, most recent candlestick is returned.
        """

        url = self.BASE_URL + '/api/v3/klines'

        if not params.get('symbol') or not params.get('interval'):
            err_msg = 'Both symbol and interval parameters have to be passed to method.'
            raise NotEnoughArguments(err_msg)

        res = requests.get(url, params=params)
        try:
            res.raise_for_status()
            data_row = res.json()
        except Exception as e:
            print(f'Some exception was caught while making request to url: {url}')
            print(f'Exception - {e}')
            sys.exit(1)

        return [{
            'time_open': datetime.fromtimestamp(candlestick[0] / 1000).strftime('%Y-%m-%d %H:%M'),
            'time_close': datetime.fromtimestamp(candlestick[6] / 1000).strftime('%Y-%m-%d %H:%M'),
            'price_open': float(candlestick[1]),
            'price_high': float(candlestick[2]),
            'price_low': float(candlestick[3]),
            'price_close': float(candlestick[4]),
        } for candlestick in data_row]

    def sync_with_server(self, interval):
        sleep_time = 10

        return sleep_time

    @staticmethod
    def is_file_updated(filename, max_age: int = 24) -> bool:
        """
            Return if is older than `max_age` or not.
            We assume, file already exists

            filename: name_of_file [str]
            max_age: last_file_modification [int] #TODO -> More time formats
        """

        age_ms = max_age * 3600.0
        timestamp_now = datetime.timestamp(datetime.now())
        timestamp_file = os.path.getmtime(filename)

        return timestamp_now - age_ms < timestamp_file
