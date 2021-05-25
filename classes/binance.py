import os

from binance.client import Client
from datetime import datetime


class Binance:

    def __init__(self):
        self.API_KEY = os.environ['BINANCE_API_KEY']
        self.API_SECRET = os.environ['BINANCE_API_SECRET']

        # Instance of Binance client
        self.client = Client(self.API_KEY, self.API_SECRET)

        # Dictionary ->
        # {
        #     'price': price [str],
        #     'symbol': coin_pair [str]
        # }
        self.coins_info = self.client.get_all_tickers()
        self.coins_file_path = 'data/coin_pairs.txt'

    def get_coin_pairs(self, base_currency='USDT'):
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

    @staticmethod
    def is_file_updated(filename, max_age=24):
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
