import requests
from util import hook
import urllib
from random import choice
import json


def url_short(url):
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post('https://www.googleapis.com/urlshortener/v1/url', data=json.dumps(payload), headers=headers)
    data = json.loads(r.content)
    url = data['id']
    return url

@hook.command('ks')
@hook.command
def kickstarter(inp, chan=None, say=None):
    base_url = 'http://www.kickstarter.com/projects/search.json?search=&term='
    url = base_url + urllib.quote_plus(inp)
    kjson = requests.get(url).json

    if len(kjson['projects']) == 0:
        return "Search returned nothing. Sorry :("

    entry = choice(kjson['projects'])
    blurb = entry['blurb'][0:125] + '...'
    url = url_short(entry['urls']['web']['project'])
    goal = "${:,.2f} / ${:,.2f}".format(entry['pledged'], entry['goal'])
    status = entry['state'].upper()
    backers = entry['backers_count']

    try:
        return "{3} :: {0} :: {1} :: {2} :: {4} ({5} Backers)".format(entry['name'], blurb, url, goal, status, backers)
    except:
        return "KickStarter Shat Out An Error. Try again."

