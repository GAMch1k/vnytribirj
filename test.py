import coins_parser
from binance.spot import Spot
import json

client = Spot()

coins = list(set(coins_parser.parse_coins()))
print(len(coins))
# print(coins)


coins_2 = []

for i in coins:
    coins_2.append(i.upper())

for i in coins:
    print(client.book_ticker(i.upper()[:-3] + 'BUSD'))

# print(client.book_ticker(coins_2))



