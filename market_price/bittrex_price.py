from bittrex.bittrex import Bittrex


def get_bittrex_price(market, hm_orders=12, book='Buy'):
    """
    :param market: 'BTC-FTC'
    :param hm_orders:
    :param book:
    :return:
    """
    lst = market.split('_')
    if lst[1] == 'BTC':
        market = 'BTC-' + lst[0]
    print('Market: {}'.format(market))
    my_bittrex = Bittrex(None, None)
    ret = my_bittrex.get_ticker(market)
    result = ret.get('result')
    if result:
        return float(result['Last'])
    else:
        raise Exception("error in get_bittrex_price: {}".format(ret))
