from util import hook, http
import json, random, re

twitch_api_url = 'https://api.twitch.tv/kraken/'
twitch_re = (r'(?:twitch.*?(?:/))'
             '([-_a-z0-9]+)', re.I)

@hook.command(autohelp=False)
def twitch(inp,top=None,api_key=None):
    '.twitch [game [rand]|user] <query> -- returns a specified channel, a random/top stream for a specified game '\
    'or a general search. If no paramaters, returns a random stream.'
	    
    if inp.startswith('game '):
        query = inp.replace('game ','')
        if query.startswith('rand '):
            query = query.replace('rand ','')
            rand = '1'
        return search_game(query,top)
    elif inp.startswith('user '):
        query = inp.replace('user ','')
        return search_user(query)
    elif not inp:
        return search_rand()
    else:
        return search_general(inp)


def search_game(query,rand=None,found=None):
    game_url = twitch_api_url + 'search/games?type=suggest&live=true&q=' + query.replace(' ','%20')
    results = json.load(http.open(game_url))
    
    if not results['games']:
       return 'No livestreams found for games matching ' + query
    game_name = results['games'][0]['name']
    search_url = twitch_api_url + 'search/streams?limit=1&q=' + game_name.replace(' ','%20')
    search_results = json.load(http.open(search_url))
    
    total = search_results['_total']
    if not rand:
       offset = 0
    while not found:
       if rand:
           offset = random.randint(0,(total-1))
       result_url = search_url + '&offset=' + str(offset)
       result = json.load(http.open(result_url))['streams'][0]
       print result['game'] + ' == ' + game_name
       if result['game'] == game_name:
           found = '1'
       elif not rand:
           offset += 1
    
    output = '[LIVE] ' + result['channel']['status'] + ' | Playing: ' + game_name + ' | ' + str(result['viewers']) + ' viewers | ' + result['channel']['url']
    return output.replace('&#39;','\'')
	
def search_user(query):
    channel_url = twitch_api_url + 'channels/' + query
    results = json.load(http.open(channel_url))
    try:
        return results['message']
    except:
        pass
 
    search_url = twitch_api_url + 'search/streams?limit=100&q=' + results['display_name']
    print search_url
    search_results = json.load(http.open(search_url))

    for i in range(0,100):
        try:
            stream = search_results['streams'][i]
            print stream['channel']['url'] + ' = ' + results['url']
            if stream['channel']['url'] == results['url']:
                output = '[LIVE] ' + results['status'] + ' | Playing: ' + stream['game'] + ' | ' +  str(stream['viewers']) + ' viewers | ' + results['url']
                return output.replace('&#39;','\'')
                
        except:
            return '[OFF] ' + results['url']

    return '[OFF] ' + results['url']

def search_rand(found=None):
    games_url = twitch_api_url + 'games/top?limit=1'
    games = json.load(http.open(games_url))
    total = games['_total']

    offset = random.randint(0,(total-1))
    rand_game_url = games_url + '&offset=' + str(offset)
    rand_game = json.load(http.open(rand_game_url))['top'][0]['game']
    
    return search_game(rand_game['name'],'1')

def search_general(query):
    search_url = twitch_api_url + 'search/streams?limit=1&q=' + query.replace(' ','%20')
    try:
        result = json.load(http.open(search_url))['streams'][0]
    except:
        return 'No results found.'
    
    output = '[LIVE] ' + result['channel']['status'] + ' | Playing: ' + result['game'] + ' | ' + str(result['viewers']) + ' viewers | ' + result['channel']['url']
    return output.replace('&#39;','\'')

@hook.regex(*twitch_re)
def twitch_url(match):
    output = search_user(match.group(1))
    last_pipe = output.rfind('|')
    return output[:(last_pipe-1)]