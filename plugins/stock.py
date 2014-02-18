import random

from util import hook, http


@hook.command
def stock(inp):
    '''.stock <symbol> -- gets stock information'''

    ret_string = ""
    symbols = []
    symbols = inp.split()

    url = ('http://query.yahooapis.com/v1/public/yql?format=json&'
           'env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys')
    
    for ticker in symbols:
      parsed = http.get_json(url, q='select * from yahoo.finance.quote '
                             'where symbol in ("%s")' % ticker)  # heh, SQLI

      quote = parsed['query']['results']['quote']

      # if we dont get a company name back, the symbol doesn't match a company
      if quote['Change'] is None:
          return "unknown ticker symbol %s" % ticker

      if quote['Change'][0] == '-':
          quote['color'] = "5"
      else:
          quote['color'] = "3"

      quote['Percent_Change'] = (100 * float(quote['Change']) /
                                 float(quote['LastTradePriceOnly']))

      ret = "%(Name)s - %(LastTradePriceOnly)s "                   \
            "\x03%(color)s%(Change)s (%(Percent_Change).2f%%)\x03 "        \
            "Day Range: %(DaysRange)s " \
            "MCAP: %(MarketCapitalization)s" % quote

      ret_string = ret_string + " | " + ret

    return ret_string
