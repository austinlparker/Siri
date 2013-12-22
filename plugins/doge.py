from util import hook
import requests
import lxml.html



@hook.command
def doge(inp, say=None):
    if inp:
        try:
            amount = int(inp)
        except:
            amount = 1000
    else:
        amount = 1000
        
    return "{1} doge is currently worth ${0}.".format(get_usd(amount), amount)


def get_usd(amount=1000):
    if type(amount) != int:
        amount = 1000
        
    r = requests.get('http://dogepay.com/frame_converter.php?v={0}&from_type=DOGE&to_type=USD'.format(amount)).text
    html = lxml.html.fromstring(r)
    amount = html.xpath('//font/text()')[0]
    return amount.split('= ')[1].replace('$', '')


if __name__ == "__main__":
    print get_usd()
