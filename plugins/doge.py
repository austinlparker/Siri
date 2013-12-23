from util import hook
import requests
import lxml.html



@hook.command
def doge(inp, say=None):
    amount = inp
    usd_amount,exchange_rate = get_usd(amount)
    return "{0} doge is currently worth ${1}. (1 doge = {2} BTC)".format(amount, usd_amount, exchange_rate)


def get_usd(amount=1000):

    try:
        amount = int(amount)
    except ValueError:
        amount = 1000

    r_btc = requests.get('http://dogepay.com/frame_converter.php?v=1&from_type=DOGE&to_type=BTC'.format(amount)).text
    r = requests.get('http://dogepay.com/frame_converter.php?v={0}&from_type=DOGE&to_type=USD'.format(amount)).text

    html_btc = lxml.html.fromstring(r_btc)
    html = lxml.html.fromstring(r)

    btc_exchange_raw = html_btc.xpath('//font/text()')[0]
    amount_raw = html.xpath('//font/text()')[0]

    btc_exchange_amt = btc_exchange_raw.split('= ')[1].replace('BTC ', '')
    amount = amount_raw.split('= ')[1].replace('$', '')
    return amount, btc_exchange_amt


if __name__ == "__main__":
    print get_usd()
