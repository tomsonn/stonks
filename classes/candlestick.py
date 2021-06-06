import math


class Candlestick:

    def __init__(self, data: dict):
        self.data = data

        self.open = data['price_open']
        self.close = data['price_close']
        self.high = data['price_high']
        self.low = data['price_low']
        self.time_open = data['time_open']
        self.time_close = data['time_close']

    def is_hammer(self):
        THRESHOLD = 0.618

        delta_candle = math.fabs(self.high - self.low)
        body_low = self.open if self.open < self.close else self.close
        delta_bottom = body_low - self.low

        return delta_bottom / delta_candle > THRESHOLD

    def get_data(self):
        return self.data
