import requests
import json


def parse_coins(pair='BTC'):

    uri = 'https://api.binance.com'
    r = requests.get(uri + '/api/v3/ticker/price')

    arr_usdt = list()
    for coin in r.json():
        if coin['symbol'][-4:] == 'BUSD':
            arr_usdt.append(coin['symbol'][:-4])
    
    # arr_btc = list()
    # for coin in r.json():
    #     if coin['symbol'][-3:] == 'BTC':
    #         arr_usdt.append(coin['symbol'][:-3])

    arr = list()
    for coin in r.json():
        if coin['symbol'][-len(pair):] == pair and coin['symbol'][:-len(pair)] in arr_usdt:
            arr.append(coin['symbol'].lower())
        
    return arr
