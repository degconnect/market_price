import os

import requests

import time
import weightedstats as ws
import requests

from cryptopia import Cryptopia
from cryptobridge import cryptobridge_api_query

eCoinsMarkets = 1
eCryptopia = 2
eOutletbit = 3
eStocksExchange = 4
eCryptoBridge = 5


EXCHANGES = (
    (eCoinsMarkets, 'CoinsMarkets'),
    (eCryptopia, 'Cryptopia'),
    (eOutletbit, 'Outletbit'),
    (eStocksExchange, 'StocksExchange'),
    (eCryptoBridge, 'Crypto Bridge')
)


def get_exchange_name(pk):
    for p, name in EXCHANGES:
        if p == pk:
            return name


def get_cryptopia_price(market, hm_orders=12, book='Buy'):
    """
    :param market: LTC_USDT ex.
    :param hm_orders: how many orders depth
    :param book: Sell or Buy
    :return:
    """
    api = Cryptopia()
    ret, error = api.get_orders(market)
    orders = ret[book]
    required_orders = orders[:hm_orders]
    prices = [float(o['Price']) for o in required_orders]
    volumes = [float(o['Volume']) for o in required_orders]
    price = ws.weighted_median(prices, volumes)
    return price


def how_much_if_sell_all_coins(market, amount_to_sell):
    """
    :param market: ex INN_BTC, LTC_USDT
    :param amount_to_sell:
    :return: (amount pf coin received after sell, real price of your operation, how many orders in book it took)
    """
    api = Cryptopia()
    ret, error = api.get_orders(market)
    orders = ret['Buy']
    available, result, i = amount_to_sell, 0, 0
    for item in orders:
        amount = min(available, item['Volume'])
        result += amount * item['Price']
        available -= amount
        i += 1
        if available <= 0:
            break
    return result, result/amount_to_sell, i


def get_stocks_exchange_price_gen():

    cache = {
        'last_call': time.time() - 10,
        'result': []
    }

    def get_stocks_exchange_price(market, hm_orders=12, book='Buy'):
        """
        :param market:
        :param hm_orders:
        :param book:
        :return:
        """
        url = 'https://stocks.exchange/api2/ticker'
        headers = {'accept': 'application/json'}
        # print("cache['last_call']: {}".format(cache['last_call']))
        # print("time.time() - cache['last_call']: {}".format(time.time() - cache['last_call']))
        items = cache['result']
        if time.time() - cache['last_call'] < 15:
            pass  # just get previous call from cache
        else:
            resp = requests.get(url, headers=headers)
            cache['last_call'] = time.time()
            if resp.status_code == 409:  # cloudflare You are being rate limited
                time.sleep(15)
                resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                items = resp.json()
                cache['result'] = items
            else:
                raise Exception('Error getting price from Stocks.Exchange. resp.status_code: {} '.format(resp.status_code))
        ret = [item['last'] for item in items if item['market_name'] == market]
        if ret:
            return float(ret[0])
        else:
            msg = "Error getting price from Stocks.Exchange. Market {} doesn't exist in  Stocks.Exchange"
            raise Exception(msg.format(market))

    return get_stocks_exchange_price


get_stocks_exchange_price = get_stocks_exchange_price_gen()


def get_cryptobridge_price_gen():
    cache = {
        'last_call': time.time() - 10,
        'result': []
    }

    def get_cryptobridge_price(market, hm_orders=12, book='Buy'):
        """
        :param market:
        :param hm_orders:
        :param book:
        :return:
        """
        # print("cache['last_call']: {}".format(cache['last_call']))
        # print("time.time() - cache['last_call']: {}".format(time.time() - cache['last_call']))
        items = cache['result']
        if time.time() - cache['last_call'] < 15:
            pass  # just get previous call from cache
        else:
            items = cryptobridge_api_query('ticker')
            print(items)
            cache['last_call'] = time.time()
            cache['result'] = items

        ret = [item['last'] for item in items if item['id'] == market]
        if ret:
            return float(ret[0])
        else:
            msg = "Error getting price from CryptoBridge Exchange. Market {} doesn't exist in CryptoBridge"
            raise Exception(msg.format(market))

    return get_cryptobridge_price


get_cryptobridge_price = get_cryptobridge_price_gen()


def get_average_price(exchange, market, hm_orders=5, book='Buy'):
    price_functions = {
        eCryptopia: get_cryptopia_price,
        eStocksExchange: get_stocks_exchange_price,
        eCryptoBridge: get_cryptobridge_price,
    }
    func = price_functions.get(exchange)
    if func is None:
        raise Exception('{} Exchange has no price function defined'.format(get_exchange_name(exchange)))
    return func(market, hm_orders, book)


def get_price(exchange, currency):
    market = '{}_BTC'.format(currency)
    return get_average_price(exchange, market=market, hm_orders=5, book='Buy')
