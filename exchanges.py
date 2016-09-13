import requests
import datetime
import pandas as pd

# Currenzy
# btc_cad
# btc_usd
# eth_btc
# eth_cad


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
        self.ticker
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
    """
    def __init__(self, ticker, provider, timestamp, data):
        self.ticker
        self.provider = provider
        self.timestamp = timestamp
        self.sell = data['sell']
        self.buy = data['buy']

    def __str__(self):
        return "{} Transaction for {} collected at {}".format(self.ticker,
                                                              self.provider,
                                                              self.timestamp)


class QuadrigaxCollector(object):

    NAME = 'Quadrigax'

    # Curl function
    def _make_request(self, api, postdict=None, timeout=8):
        BASE_URL = "https://api.quadrigacx.com/v2/"
        url = BASE_URL + api

        if postdict:
            r = requests.get(url, params=postdict, timeout=8)
        else:
            r = requests.get(url, timeout=8)
        return r.json()

    # Collection raw information
    def _get_raw_book(self, ticker):
        api = 'order_book?book={}'.format(ticker)
        return self._make_request(api=api)

    def _get_raw_price(self, ticker):
        api = 'ticker?book={}'.format(ticker)
        return self._make_request(api=api)

    def _get_raw_transaction(self, ticker):
        api = 'transactions?book={}'.format(ticker)
        return self._make_request(api=api)

    # Clean raw information
    def _clean_book(self, raw_data):
        pass

    def _clean_price(self, raw_data):
        pass

    def _clean_transaction(self, raw_data):
        dict_return = dict(sell=[], buy=[])
        for val in raw_data:
            if val['side'] == 'sell':
                dict_return['sell'].append(val)
            elif val['side'] == 'buy':
                dict_return['buy'].append(val)
            else:
                raise ValueError("Malformed data in raw transaction")
        return dict_return

    # Collect information
    def get_book(self, ticker='btc_cad'):

        raw = self._get_raw_book(ticker)
        # No cleaning. Quad book is clean
        order = OrderBook(ticker=ticker,
                          provider=self.NAME,
                          timestamp=datetime.datetime.now(),
                          data=raw)

        return order

    def get_price(self, ticker='btc_cad'):

        raw = self._get_raw_price(ticker)
        # No cleaning. Quad price is clean
        price = Price(ticker=ticker,
                      provider=self.NAME,
                      timestamp=datetime.datetime.now(),
                      data=raw)

        return price

    def get_transaction(self, ticker='btc_cad'):

        raw = self._get_raw_transaction(ticker)
        clean = self._clean_transaction(raw)

        transac = Transaction(ticker=ticker,
                              provider=self.NAME,
                              timestamp=datetime.datetime.now(),
                              data=clean)

        return transac

class CoinsquareCollector(object):

    NAME = 'Coinsquare'

    def _make_request(self, api, postdict=None, timeout=8):
        BASE_URL = "https://coinsquare.io"
        url = BASE_URL + api

        if postdict:
            r = requests.get(url, params=postdict, timeout=8)
        else:
            r = requests.get(url, timeout=8)
        return r.json()

    # Collection raw information
    def _get_raw_book(self, ticker):
        api = '?method=book&ticker=CAD&base=BTC'
        return self._make_request(api=api)

    def _get_raw_price(self, ticker):
        api = '?method=quotes'
        return self._make_request(api=api)

    # Coinbase doesn't have transaction API     
    def _get_raw_transaction(self, ticker):
        pass

    # Clean raw information
    def _clean_book(self, raw_data):
        pass

    def _clean_price(self, raw_data):
        pass

    def _clean_transaction(self, raw_data):
        dict_return = dict(sell=[], buy=[])
        for val in raw_data:
            if val['side'] == 'sell':
                dict_return['sell'].append(val)
            elif val['side'] == 'buy':
                dict_return['buy'].append(val)
            else:
                raise ValueError("Malformed data in raw transaction")
        return dict_return

    # Public method - Collect information
    def get_book(self, ticker='btc_cad'):

        raw = self._get_raw_book(ticker)
        # No cleaning. Quad book is clean
        order = OrderBook(ticker=ticker,
                          provider=self.NAME,
                          timestamp=datetime.datetime.now(),
                          data=raw)

        return order

    def get_price(self, ticker='btc_cad'):

        raw = self._get_raw_price(ticker)
        # No cleaning. Quad price is clean
        price = Price(ticker=ticker,
                      provider=self.NAME,
                      timestamp=datetime.datetime.now(),
                      data=raw)

        return price

    def get_transaction(self, ticker='btc_cad'):

        raw = self._get_raw_transaction(ticker)
        clean = self._clean_transaction(raw)

        transac = Transaction(ticker=ticker,
                              provider=self.NAME,
                              timestamp=datetime.datetime.now(),
                              data=clean)

        return transac





quad = QuadrigaxCollector()
book = quad.get_book()
price = quad.get_price()
transac = quad.get_transaction()

print(price)

raw_price = quad._get_raw_price('btc_cad')

print(raw_price)



raw_transact = quad._get_raw_transaction('btc_cad')
clean_transact = quad._clean_transaction(raw_transact)
print(clean_transact)


print(dict_return)

print(raw_transact)

print(book)
print(book.bids)
print(book.ask)
print(quad.NAME)

quad_book = quad.get_book()

print(quad_book)
print(quad_book.data)



coinsquare = Coinsquare()
coin_book = coinsquare.get_book()
print(coin_book.keys())
print(coin_book['book'])
print(coin_book['sales'])
print(coinsquare.get_book())



class QuadrigaxCollector(object):

    NAME = 'Coinsquare'

    def _make_request(self, api, postdict=None, timeout=8):
        BASE_URL = "https://coinsquare.io"
        url = BASE_URL + api

        if postdict:
            r = requests.get(url, params=postdict, timeout=8)
        else:
            r = requests.get(url, timeout=8)
        return r.json()

    def get_book(self, ticker='btc_cad'):
        api = '?method=book&ticker=CAD&base=BTC'
        return self._make_request(api=api)

    def get_price(self, ticker='btc_cad'):
        api = '?method=quotes'
        return self._make_request(api=api)

    # def get_transaction(self, ticker='btc_cad'):
    #     api = 'transactions?book={}'.format(ticker)
    #     return self._make_request(api=api)


# def get_book(ticker):
#     r = requests.get(BASE_URL+'order_book?book={}'.format(ticker))
#     return r.json()


# def get_price(ticker):
#     r = requests.get(BASE_URL+'ticker?book={}'.format(ticker))
#     return r.json()


# def get_transaction(ticker):
#     r = requests.get(BASE_URL+'transactions?book={}'.format(ticker))
#     return r.json()


def list_to_df(data_list, columns):
    df_list = pd.DataFrame(data_list)
    df_list.columns = columns
    return df_list

# Clean book
book = get_book(ticker='btc_cad')

df_bids = list_to_df(book['bids'], ['price', 'volume'])
df_asks = list_to_df(book['asks'], ['price', 'volume'])






print(transactions[0])



>>> {'amount': '0.01628140', 'date': '1473536255', 'side': 'sell', 'tid': 287406, 'price': '810.00'}
for val in transactions:
    print("Date: {}\n Price: {}\n Amount: {}\n Side: {}\n TickerID: {}".format(val['date'], val['price'], val['amount'], val['side'], val['tid']))


price = get_price(ticker='btc_cad')
transactions = get_transaction(ticker='btc_cad')

print(datetime.datetime.fromtimestamp(1473536255))

print(price)
print(transactions)
print(book['asks'])
print(book['bids'])

https://api.quadrigacx.com/v2/ticker?book=XXX



https://api.quadrigacx.com/v2/order_book?book=btc_cad