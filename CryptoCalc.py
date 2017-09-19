#!/usr/bin/env python3

import json
from urllib.request import urlopen


class font:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def getCoinData(url):
    page = urlopen(url)
    str_data = page.read()
    json_data = json.loads(str_data.decode('utf-8'))
    return json_data


def makeCoinDict(json_data):
    coin_dict = {}
    for coin in json_data:
        name = coin['name'].upper()
        symbol = coin['symbol'].upper()
        price = float(coin['price_usd'])

        coin_dict[name] = price
        coin_dict[symbol] = price

    return coin_dict


def getCommand():
    print('Please select a command (see manual for usage):')
    print(font.BOLD + 'L' + font.END + 'oad,',\
            font.BOLD + 'S' + font.END + 'ave,',\
            font.BOLD + 'A' + font.END + 'dd,',\
            font.BOLD + 'D' + font.END + 'elete,',\
            font.BOLD + 'R' + font.END + 'eport,',\
            font.BOLD + 'E' + font.END + 'xit.')
    user_in = input('$:').upper().split(' ')
    command, params = user_in[0], user_in[1:]
    return command, params


def executeCommand(command, params, portfolio, coin_dict):
    if (command=='L' or command=='LOAD'):
        with open('portfolios/default.json', 'r') as f:
            portfolio = json.load(f)
    if (command=='S' or command=='SAVE'):
        with open('portfolios/default.json', 'w') as f:
            json.dump(portfolio, f)
    if (command=='A' or command=='ADD'):
        coin, amt = params
        if coin not in portfolio:
            portfolio[coin] = 0
        portfolio[coin] += float(amt)
    if (command=='D' or command=='DELETE'):
        coin, amt = params
        portfolio[coin] -= float(amt)
    if (command=='R' or command=='REPORT'):
        print('Portfolio:')
        total = 0.0
        for coin, amt in portfolio.items():
            print(coin, ':', amt, '($%.2f)' % (coin_dict[coin]*amt))
            total += coin_dict[coin] * amt
        print('Total: $%.2f' % total)
    if (command=='E' or command=='EXIT'):
        return portfolio, True
    return portfolio, False


if __name__ == '__main__':
    # URL for Coin Market Cap API
    CMC_api_url = 'https://api.coinmarketcap.com/v1/ticker/'

    print('Obtaining Crypto Coin Prices...')
    coin_data = getCoinData(CMC_api_url)
    coin_dict = makeCoinDict(coin_data)
    print('Done.')

    portfolio = {}
    while(True):
        command, params = getCommand()
        portfolio, exit = executeCommand(command, params, portfolio, coin_dict)
        if exit:
            break

    print('Goodbye.')
