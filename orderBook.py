# import time
from create_db import DBOrderBook, DBOrderPull, DBPrice, DBTransactPull, DBTransaction

class OrderBook(object):
    """
    data must be a dictionary with two keys
    ['bids', 'asks']
    the value must be a list of list.
    Invidual list element contains
    two values [value, amount]
    """

    def __init__(self, ticker, provider, timestamp, data):
        self.ticker = ticker
        self.provider = provider
        self.timestamp = timestamp
        self.bids = data['bids']
        self.asks = data['asks']

    def store(self, session):

        new_pull = DBOrderPull()
        # Create book_id from timestamp
        # book_id = int(time.mktime(self.timestamp.timetuple()))
        new_pull.timestamp = self.timestamp
        new_pull.ticker = self.ticker
        new_pull.provider = self.provider
        session.add(new_pull)
        session.commit()
        # Once commited extract the book_id
        book_id = new_pull.book_id

        for val, side in [(self.bids, 'bid'), (self.asks, 'ask')]:
            for el in val:
                new_book = DBOrderBook()
                new_book.book_id = book_id
                new_book.price = el[0]
                new_book.amount = el[1]
                new_book.side = side
                session.add(new_book)
                session.commit()

    def __str__(self):
        return "{} OrderBook for {} collected at {}".format(self.ticker,
                                                            self.provider,
                                                            self.timestamp)


class Price(object):
    """
    last - last BTC price
    high - last 24 hours price high
    low - last 24 hours price low
    volume - last 24 hours volume
    bid - highest buy order
    ask - lowest sell order
    """
    def __init__(self, ticker, provider, timestamp, data):
        self.ticker = ticker
        self.provider = provider
        self.timestamp = timestamp
        self.last = data['last']
        self.high = data['high']
        self.low = data['low']
        self.volume = data['volume']
        self.bid = data['bid']
        self.ask = data['ask']

    def store(self, session):
        new_price = DBPrice()
        new_price.ticker = self.ticker
        new_price.provider = self.provider
        new_price.timestamp = self.timestamp
        new_price.last = self.last
        new_price.high = self.high
        new_price.low = self.low
        new_price.volume = self.volume
        new_price.bid = self.bid
        new_price.ask = self.ask
        session.add(new_price)
        session.commit()

    def __str__(self):
        return "{} Price for {} collected at {}".format(self.ticker,
                                                        self.provider,
                                                        self.timestamp)


class Transaction(object):
    """
    date - unix timestamp date and time
    tid - transaction id
    price - BTC price
    amount - BTC amount
    side - The trade side indicates the maker order side
    (maker order is the order that was open on the order book)
    data is a list of list containing the above mentionned
    elements
    """
    def __init__(self, ticker, provider, timestamp, data):
        self.ticker = ticker
        self.provider = provider
        self.timestamp = timestamp
        self.data = data

    def store(self, session):
        new_pull = DBTransactPull()
        new_pull.timestamp = self.timestamp
        new_pull.ticker = self.ticker
        new_pull.provider = self.provider
        session.add(new_pull)
        session.commit()
        transact_id = new_pull.transact_id

        for val in self.data:
            new_transact = DBTransaction()
            new_transact.transact_id = transact_id
            new_transact.trade_date = val[0]
            new_transact.tid = val[1]
            new_transact.price = val[2]
            new_transact.amount = val[3]
            new_transact.side = val[4]
            session.add(new_transact)
            session.commit()

    def __str__(self):
        return "{} Transaction for {} collected at {}".format(self.ticker,
                                                              self.provider,
                                                              self.timestamp)
