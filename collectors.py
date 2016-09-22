import requests
import datetime
import time
from orderBook import OrderBook, Price, Transaction

class QuadrigaxCollector(object):
    # Currency
    # btc_cad
    # btc_usd
    # eth_btc
    # eth_cad
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
        dict_return = {}
        for key in ['bids', 'asks']:
            clean = [[float(x[0]), float(x[1])] for x in raw_data[key]]
            dict_return[key] = clean
        return dict_return

    def _clean_price(self, raw_data):
        dict_return = {key: float(val) for key, val in raw_data.items()}
        return dict_return

    def _clean_transaction(self, raw_data):
        list_return = []
        for idx, val in enumerate(raw_data):
            price = float(val['price'])
            amount = float(val['amount'])
            date = datetime.datetime.fromtimestamp(int(val['date']))
            side = val['side']
            num = idx
            list_return.append([date, num, price, amount, side])
        return list_return

    # Collect information
    def get_book(self, ticker='btc_cad'):

        raw = self._get_raw_book(ticker)
        clean = self._clean_book(raw)
        order = OrderBook(ticker=ticker,
                          provider=self.NAME,
                          timestamp=datetime.datetime.now(),
                          data=clean)

        return order

    def get_price(self, ticker='btc_cad'):

        raw = self._get_raw_price(ticker)
        clean = self._clean_price(raw)
        price = Price(ticker=ticker,
                      provider=self.NAME,
                      timestamp=datetime.datetime.now(),
                      data=clean)

        return price

    def get_transaction(self, ticker='btc_cad'):

        raw = self._get_raw_transaction(ticker)
        clean = self._clean_transaction(raw)

        transac = Transaction(ticker=ticker,
                              provider=self.NAME,
                              timestamp=datetime.datetime.now(),
                              data=clean)

        return transac


def correct_amt(amt):
    if amt == '':
        amt = 0
    return int(amt) / float(100)


def correct_num(n):
    if n == '':
        n = 0
    return int(n) / float(100000000)


def find_price(amt, n):
    if n == 0:
        return 0
    return float(amt) / float(n)


def get_values(amt, n):
    amt = correct_amt(amt)
    n_bitcoin = correct_num(n)
    price = find_price(amt, n_bitcoin)
    return [price, n_bitcoin]


class CoinsquareCollector(object):

    NAME = 'Coinsquare'
    dict_transact_map = {'b': 'buy', 's': 'sell'}

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
        split = ticker.split("_")
        api = '?method=book&ticker={0}&base={1}'.format(split[1].upper(), split[0].upper())
        return self._make_request(api=api)

    def _get_raw_price(self, ticker):
        api = '?method=quotes'
        return self._make_request(api=api)

    # Coinbase include transaction in the book
    def _get_raw_transaction(self, ticker):
        pass

    # Clean raw information
    def _clean_book(self, raw_data):
        dict_return = dict(bids=[], asks=[])
        for val in raw_data['book']:
            if val['t'] == 's':
                key = 'bids'
            elif val['t'] == 'b':
                key = 'asks'
            else:
                raise ValueError("Malformed book")
            data = get_values(val['amt'], val['base'])
            dict_return[key].append(data)
        return dict_return

    def _clean_price(self, raw_data):
        for val in cp['quotes']:
            if val['base'] == 'CAD' and val['ticker'] == 'BTC':
                dict_return = dict(last=correct_amt(val['last']), 
                    high=correct_amt(val['high24']), 
                    low=correct_amt(val['low24']), 
                    volume=correct_num(val['volbase']), 
                    bid=correct_amt(val['bid']), 
                    ask=correct_amt(val['ask']))
                return dict_return

    def _clean_transaction(self, raw_data):
        list_return = []
        for val in raw_data['sales']:
            values = get_values(val['amt'], val['base'])
            price = values[0]
            amount = values[1]
            date = datetime.datetime.strptime(val['date'], "%Y-%m-%d %H:%M")
            side = self.dict_transact_map[val['t']]
            num = int(val['i'])
            list_return.append([date, num, price, amount, side])
        return list_return

    # Public method - Collect information
    def get_book(self, ticker='btc_cad'):

        raw = self._get_raw_book(ticker)
        clean_book = self._clean_book(raw)
        clean_transac = self._clean_transaction(raw)

        order = OrderBook(ticker=ticker,
                          provider=self.NAME,
                          timestamp=datetime.datetime.now(),
                          data=clean_book)

        transac = Transaction(ticker=ticker,
                              provider=self.NAME,
                              timestamp=datetime.datetime.now(),
                              data=clean_transac)

        return order, transac

    def get_price(self, ticker='btc_cad'):

        raw = self._get_raw_price(ticker)
        clean = self._clean_price(raw)
        price = Price(ticker=ticker,
                      provider=self.NAME,
                      timestamp=datetime.datetime.now(),
                      data=clean)

        return price












