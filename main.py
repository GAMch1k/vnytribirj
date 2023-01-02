import coins_parser
import scanner
import threading
import time 


def main():
    coins = coins_parser.parse_coins('BTC')
    print(len(coins))
    # print(coins)

    for coin in coins:
        print(coin)
        threading.Thread(target=scanner.scan_coin, args=(coin,)).start()
        # time.sleep(0.1)

    while True:
        try:
            time.sleep(5)
            scanner.calculate_profit()
            scanner.dump_data()
        except:
            pass

if __name__ == '__main__':
    main()
