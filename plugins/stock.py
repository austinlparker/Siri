from util import hook
import requests


def yahoo_stocks(symbol):
    base_url = "http://download.finance.yahoo.com/d/quotes.csv"
    parameters = {
        's': symbol,
        'e': '.csv',
        'f': 'sncl1'
    }
    r = requests.get(base_url, params=parameters)
    stock_data = r.content.replace('"', '').strip().replace(' - ', ',').split(',')
    stock_description = ['symbol', 'name', 'change', 'change_percent', 'price']
    stock = dict(zip(stock_description, stock_data))
    return stock
    
   
@hook.command
def stock(inp):
    symbol = inp.split(' ')[0]
    stock = yahoo_stocks(symbol)
    
    return '{name} ({symbol}) :: ${price} :: {change} ({change_percent})'.format(**stock)


if __name__ == '__main__':
    y = yahoo_stocks('aapl')
    print y
