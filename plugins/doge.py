from util import hook
import requests
import lxml.html



@hook.command
def doge(inp, say=None):
    return "1000 doge is currently worth ${0}.".format(get_usd())


def get_usd():
    r = requests.get('http://dogepay.com/frame_converter.php?v=1000&from_type=DOGE&to_type=USD').text
    html = lxml.html.fromstring(r)
    amount = html.xpath('//font/text()')[0]
    return amount.split('= ')[1].replace('$', '')


if __name__ == "__main__":
    print get_usd()
