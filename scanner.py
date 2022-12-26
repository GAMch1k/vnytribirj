import time
import logging
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from binance.lib.utils import config_logging
import os, certifi, win32api
from binance.websocket.spot.websocket_client \
    import SpotWebsocketClient as WebsocketClient


os.environ['SSL_CERT_FILE'] = certifi.where()
config_logging(logging, logging.DEBUG)

my_client = Client()
my_client.start()


coins_data = {}


def message_handler(data):
    # logging.info(message)
    print(data)
    name = data['data']['s']
    coins_data[name] = data


def scan_coin(coin=None, pairs=('BTC', 'USDT')):

    if coin == None:
        logging.error('EXPECTED COIN')
        return
    
    symbols = [coin + '@ticker', coin[:-len(pairs[0])] + pairs[1].lower() + '@ticker']
    
    
    my_client.instant_subscribe(
        symbols, callback=message_handler
    )

    time.sleep(5) 

    logging.debug("closing ws connection")
    my_client.stop()
    print(coins_data)
