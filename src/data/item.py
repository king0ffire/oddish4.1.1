import numpy as np

from src.config.definitions import TIMESTAMP, STEAM_SELL_TAX, EXCHANGE


class Item:

    def __init__(self, buff_id, name, price, sell_num, steam_url, steam_predict_price, buy_max_price):
        self.id = buff_id
        self.name = name
        self.price = float(price)
        self.sell_num = int(sell_num)
        self.steam_url = steam_url
        self.steam_predict_price = float(steam_predict_price)
        self.buy_max_price = float(buy_max_price)

        # be overridden later with real history price
        self.gap = self.steam_predict_price - self.price
        self.gap_percent = self.gap * 1.0 / self.price
        self.crawl_time = TIMESTAMP

        # set history price later
        self.history_prices = []
        self.history_sold = 0
        self.history_days = 0
        self.average_sold_price = 0
        self.average_sold_price_after_tax = 0

    def set_history_prices(self, prices, days):
        self.history_prices = prices
        self.history_sold = len(prices)
        self.history_days = days
        self.average_sold_price = self.centered_average(prices)
        self.average_sold_price_after_tax = self.average_sold_price * (1 - STEAM_SELL_TAX)
        self.average_sold_price_after_tax_exchange = self.average_sold_price_after_tax / EXCHANGE  # steam卖到手价
        self.gap = self.average_sold_price_after_tax_exchange - self.price
        self.gap_percent = self.gap * 1.0 / self.price
        self.discount_percent = self.price / self.average_sold_price_after_tax_exchange

    def detail(self):
        return "{}: {}(newest sold price after tax and exchange)(origin sold price :{}) - {}(buff) = {}(beyond {:.2%}, {:.2%}). " \
               "Sold {} items in {} days.\n steam url:{}\n buff url: https://buff.163.com/market/goods?goods_id={}&from=market#tab=selling" \
            .format(
            self.name,
            '%.2f' % self.average_sold_price_after_tax_exchange,
            '%.2f' % self.average_sold_price,
            self.price,
            self.gap,
            self.gap_percent,
            self.discount_percent,
            self.history_sold,
            self.history_days,
            self.steam_url,
            self.id
        )

    def to_dict(self):
        item_dict = {
            # id is index, not content column
            # "id": self.id,
            "name": self.name,
            "price": self.price,
            "sell_num": self.sell_num,
            "steam_url": self.steam_url,
            "steam_predict_price": self.steam_predict_price,
            "buy_max_price": self.buy_max_price,
            "gap": self.gap,
            "gap_percent": self.gap_percent,
            "crawl_time": self.crawl_time,
            "history_prices": self.history_prices,
            "history_sold": self.history_sold,
            "history_days": self.history_days,
            "average_sold_price": self.average_sold_price,
            "average_sold_price_after_tax": self.average_sold_price_after_tax
        }
        return item_dict

    @staticmethod
    def centered_average(numbers):
        return numbers[0] if len(numbers) != 0 else 0
        # return np.percentile(numbers, 25) if len(numbers) != 0 else 0
