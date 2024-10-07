import random 
import time


class OTCGraphGenerator:
    def __init__(self, initial_price, volatility_percent, trend_strength):
        self.price = initial_price
        self.volatility_percent = volatility_percent
        self.trend_strength = trend_strength
        self.trend = "sideways"
        self.trend_duration = 0
        self.max_trend_duration = 100
        self.tick = 0
        self.price_history = []
        self.start_time = int(time.time())

    def update(self):
        self.tick += 1
        self.update_trend()
        self.update_volatility()
        self.update_price()
        current_time = self.start_time + (self.tick * 5)  # 5 seconds per tick
        self.price_history.append((current_time, self.price))
        return self.price

    def update_trend(self):
        self.trend_duration += 1
        if self.trend_duration >= self.max_trend_duration:
            self.change_trend()
        elif random.random() < 0.02:  # 2% chance of changing trend each update
            self.change_trend()

    def change_trend(self):
        trends = ["up", "down", "sideways"]
        weights = [0.3, 0.3, 0.4]
        self.trend = random.choices(trends, weights=weights)[0]
        self.trend_duration = 0
        self.max_trend_duration = random.randint(50, 200)
        self.trend_strength = random.uniform(0.0001, 0.001)

    def update_volatility(self):
        self.volatility_percent *= random.uniform(0.95, 1.05)
        self.volatility_percent = max(0.1, min(5, self.volatility_percent))

    def update_price(self):
        trend_factor = {"up": 1, "down": -1, "sideways": 0}[self.trend]
        trend_change = self.trend_strength * trend_factor
        volatility_value = self.price * (self.volatility_percent / 100)
        volatility_change = random.gauss(0, volatility_value)
        self.price += trend_change * self.price + volatility_change
        self.price = max(0.01, self.price)

    def generate_candles_for_apexcharts(self, candle_size=10):
        candles = []
        for i in range(0, len(self.price_history), candle_size):
            candle_data = self.price_history[i:i+candle_size]
            if len(candle_data) == candle_size:
                times, prices = zip(*candle_data)
                candles.append({
                    'x': times[0] * 1000,  # ApexCharts expects time in milliseconds
                    'y': [prices[0], max(prices), min(prices), prices[-1]]  # [open, high, low, close]
                })
        return candles