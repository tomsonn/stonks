import math
from datetime import datetime


interval_to_ms = {
    '5m': 5 * 60 * 1000,
    '15m': 15 * 60 * 1000,
    '30m': 30 * 60 * 1000,
    '1h': 60 * 60 * 1000,
    '2h': 2 * 60 * 60 * 1000,
    '4h': 4 * 60 * 60 * 1000,
    '1d': 24 * 60 * 60 * 1000
}


class Candlestick:

    def __init__(self, idx: int, data: dict, interval: str, max_candles_no: int = 500):
        self.idx = idx
        self.data = data

        self.open = data['price_open']
        self.close = data['price_close']
        self.high = data['price_high']
        self.low = data['price_low']
        self.time_open = data['time_open']
        self.time_close = data['time_close']

        self.interval = interval
        self.max_candles_no = max_candles_no

        self.is_support = False
        self.is_resistance = False

    def get_data(self):
        return self.data

    def is_hammer(self):
        THRESHOLD = 0.618

        delta_candle = math.fabs(self.high - self.low)
        body_low = self.open if self.open < self.close else self.close
        delta_bottom = body_low - self.low

        try:
            ratio = delta_bottom / delta_candle
        except ZeroDivisionError as e:
            raise e

        return ratio > THRESHOLD

    def is_in_timerange(self, time_range):
        ts_now = round(datetime.timestamp(datetime.now()) * 1000)
        ts_lower_bound = ts_now - interval_to_ms[self.interval] * time_range
        ts_candlestick = datetime.timestamp(datetime.strptime(self.time_open, '%Y-%m-%d %H:%M')) * 1000

        return ts_candlestick > ts_lower_bound

    def get_support_area(self, candles):
        """
            Decide whether discussed candlestick makes resistance level or not
            and return area between opening / closing of the candle and high / low of the candle.

            Following statement is applied for both support and resistance levels
            and these levels are made by `fractals` - 5 candles patterns.
            For support, the third candle has the lowest `low` price, the previous candles
            have decreasing lows and the next candles have increasing lows.
            Then the low of the third candle is the support level.
            The same concept can be applied to resistance levels, where the third has the highest `high`
            of the five ones.
        """

        if self.idx - 2 < 0 or self.idx + 2 >= self.max_candles_no:
            return

        candidates = candles[self.idx - 2: self.idx + 3]
        if self.low < candidates[1].get_data()['price_low'] < candidates[0].get_data()['price_low'] and \
           self.low < candidates[3].get_data()['price_low'] < candidates[4].get_data()['price_low']:

            body_lower = self.high
            for c in candidates:
                body_c = min([c.get_data()['price_close'], c.get_data()['price_open']])
                if body_c < body_lower:
                    body_lower = body_c

            self.is_support = True
            self.support_lower = self.low
            self.support_upper = body_lower

            self.data.update({
                'support_lower': self.support_lower,
                'support_upper': self.support_upper
            })

            return {
                'support_lower': self.support_lower,
                'support_upper': self.support_upper
            }

    def get_resistance_area(self, candles):
        """Decide whether discussed candlestick makes resistance level or not."""

        if self.idx - 2 < 0 or self.idx + 2 >= self.max_candles_no:
            return

        candidates = candles[self.idx - 2: self.idx + 3]
        if self.high > candidates[1].get_data()['price_high'] > candidates[0].get_data()['price_high'] and \
           self.high > candidates[3].get_data()['price_high'] > candidates[4].get_data()['price_high']:

            body_upper = self.low
            for c in candidates:
                body_c = max([c.get_data()['price_close'], c.get_data()['price_open']])
                if body_c > body_upper:
                    body_upper = body_c

            self.is_resistance = True
            self.resistance_lower = body_upper
            self.resistance_upper = self.high

            self.data.update({
                'resistance_lower': self.resistance_lower,
                'resistance_upper': self.resistance_upper
            })

            return {
                'resistance_lower': self.resistance_lower,
                'resistance_upper': self.resistance_upper
            }

