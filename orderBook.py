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

    def __str__(self):
        return "{} OrderBook for {} collected at {}".format(self.ticker,
                                                            self.provider,
                                                            self.timestamp)


class Price(object):
    """
    last - last BTC price
    high - last 24 hours price high
    low - last 24 hours price low
    vwap - last 24 hours volume weighted average price: vwap
    volume - last 24 hours volume
    bid - highest buy order
    ask - lowest sell order
    """
    def __init__(self, ticker, provider, timestamp, data):
        self.ticker = ticker
        self.last = data['last']
        self.high = data['high']
        self.low = data['low']
        self.vwap = data['vwap']
        self.volume = data['volume']
        self.bid = data['bid']
        self.ask = data['ask']

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

    def __str__(self):
        return "{} Transaction for {} collected at {}".format(self.ticker,
                                                              self.provider,
                                                              self.timestamp)
