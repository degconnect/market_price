import requests


def cryptobridge_api_query(method, params=None):
    uri = "https://api.crypto-bridge.org/api/v1/{}".format(method)
    if params is None:
        params = {}
    headers = {'accept': 'application/json'}
    resp = requests.get(uri, params=params, headers=headers)
    if resp.status_code == 200:
        return resp.json()
