import time
import logging
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from binance.lib.utils import config_logging
import os, certifi, win32api
from binance.websocket.spot.websocket_client \
    import SpotWebsocketClient as WebsocketClient
from binance.spot import Spot
import json


client = Spot()

os.environ['SSL_CERT_FILE'] = certifi.where()
config_logging(logging, logging.DEBUG)

my_client = Client()
my_client.start()


coins_data = {}


def calculate_profit():
    btcbusd = client.book_ticker('BTCBUSD')
    final = {}
    for coin in coins_data:
        try:
            # print(coins_data[coin][coin + 'BUSD']['a'])
            c = 1 / float(coins_data[coin][coin + 'BUSD']['a'])
            b = c * float(coins_data[coin][coin + 'BTC']['b'])
            u = b * float(btcbusd['askPrice'])
            prof = u - 1
            perc = prof * 100
            if perc > 0:
                final[coin] = {
                                'prof': prof, 
                                'perc': perc
                            }
        except Exception as e:
            print(coin, e)
    

    # Start from BTC
    for coin in coins_data:
        try:
            # print(coins_data[coin][coin + 'BUSD']['a'])
            b = 1 / float(btcbusd['bidPrice'])
            c = b / float(coins_data[coin][coin + 'BTC']['a'])
            u = c * float(coins_data[coin][coin + 'BUSD']['b'])
            prof = u - 1
            perc = prof * 100
            if perc > 0:
                final[coin + ' (BTC)'] = {
                                'prof': prof, 
                                'perc': perc
                            }
        except Exception as e:
            print(coin, e)
    
    with open('jsons/profits.json', 'w') as f:
        json.dump(final, f, indent=4)


def dump_data():
    with open('jsons/dump.json', 'w') as f:
        json.dump(coins_data, f, indent=4)



def message_handler(data):
    # logging.info(message)
    print(data)

    name = data['data']['s']
    name_c = ''
    name_s = ''
    if 'BUSD' in name:
        name_c = name[:-4]
        name_s = 'BUSD'
    else:
        name_c = name[:-3]
        name_s = 'BTC'
    
    print(name_c, name)
    exist = False
    for i in coins_data:
        if i == name_c:
            exist = True
    
    if not exist:
        coins_data[name_c] = {
                                name_c + 'BUSD': {}, 
                                name_c + 'BTC': {}
                            }

    coins_data[name_c][name] = data['data']

    # if coins_data[name_c][name] and coins_data[name_c][name_c + name_s]:
    #     pass
        # calculate_profit()


def scan_coin(coin=None, pairs=('BTC', 'BUSD')):

    if coin == None:
        logging.error('EXPECTED COIN')
        return
    
    symbols = [coin + '@ticker', coin[:-len(pairs[0])] + pairs[1].lower() + '@ticker']
    
    
    my_client.instant_subscribe(
        symbols, callback=message_handler
    )

    time.sleep(6000) 

    logging.debug("closing ws connection")
    my_client.stop()
    print(coins_data)
