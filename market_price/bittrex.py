from bittrex.bittrex import Bittrex


def get_bittrex_price(market, hm_orders=12, book='Buy'):
    """
    :param market: 'BTC-FTC'
    :param hm_orders:
    :param book:
    :return:
    """
    my_bittrex = Bittrex(None, None)
    return my_bittrex.get_ticker(market)
