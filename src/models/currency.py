class Currency:
    def __init__(self, base, currency_pair, sell, buy, min, max, open, last_closing, date):
        self.base = base
        self.currency_pair = currency_pair
        self.sell = sell
        self.buy = buy
        self.min = min
        self.max = max
        self.open = open
        self.last_closing = last_closing
        self.date = date

    def __str__(self):
        return  f'Base: {self.base}\n' \
                f'Currency pair: {self.currency_pair}\n' \
                f'Sell: {self.sell}\n' \
                f'Buy: {self.buy}\n' \
                f'Min day: {self.min}\n' \
                f'Max day: {self.max}\n' \
                f'Date: {self.date}\n' \
                f'Open market: {self.open}\n' \
                f'Close market: {self.last_closing}\n'
    
    def information(self):
        return  f'Base: {self.base}\n' \
                f'Currency pair: {self.currency_pair}\n' \
                f'Sell: {self.sell}\n' \
                f'Buy: {self.buy}\n' \
                f'Min day: {self.min}\n' \
                f'Max day: {self.max}\n' \
                f'Date: {self.date}\n' \
                f'Open market: {self.open}\n' \
                f'Close market: {self.last_closing}\n'