import coins_parser
import scanner


def main():
    coins = coins_parser.parse_coins('BTC')

    print(coins[2])
    scanner.scan_coin(coins[2])


if __name__ == '__main__':
    main()
