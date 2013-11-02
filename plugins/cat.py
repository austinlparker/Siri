from util import hook
import requests



@hook.command('catte')
def cat(inp, say=None):
    r = requests.get('http://daily.cattes.us/api/get_image').text
    return r + ' -  http://daily.cattes.us/ for all your yoscat needs.'
