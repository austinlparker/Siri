import random
import urllib

from util import hook, http


@hook.api_key('giphy')
@hook.command('gif')
@hook.command
def giphy(inp, api_key=None):
    '''.gif/.giphy <query> -- returns first giphy search result'''
    url = 'http://api.giphy.com/v1/gifs/search'
    query = urllib.quote_plus(inp)

    try:
        response = http.get_json(url, q=query, limit=10, api_key=api_key)
    except http.HTTPError as e:
        return e.msg

    results = response.get('data')
    if results:
        return random.choice(results).get('bitly_gif_url')
    else:
        return 'no results found'
