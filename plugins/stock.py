from util import hook
import requests
import csv
import StringIO


def yahoo_stocks(symbol):
    base_url = "http://download.finance.yahoo.com/d/quotes.csv"
    parameters = {
        's': symbol,
        'e': '.csv',
        'f': 'sncl1'
    }
    r = requests.get(base_url, params=parameters)
    stock_csv = [row for row in csv.reader(StringIO.StringIO(r.content), delimiter=',')][0]
    change, percent = stock_csv[2].split(' - ')
    stock = {
        'symbol': stock_csv[0],
        'name': stock_csv[1],
        'change': change,
        'change_percent': percent,
        'price': stock_csv[3]
    }
    return stock
    
   
@hook.command
def stock(inp):
    symbol = inp.split(' ')[0]
    stock = yahoo_stocks(symbol)
    
    return '{name} ({symbol}) :: ${price} :: {change} ({change_percent})'.format(**stock)


if __name__ == '__main__':
    y = yahoo_stocks('tsla')
    print y
