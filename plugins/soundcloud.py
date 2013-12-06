#soundcloud.py
from util import hook, http
soundcloud_url = 'http://api.soundcloud.com/'

#users, search
@hook.api_key('soundcloud')
@hook.command('sc')
@hook.command()
def soundcloud(inp,api_key=None):
    ".soundcloud/.sc [user] <query> -- searches for tracks (or users if specified) for the query and returns the top result"
    if inp.startswith('user '):
        query = inp.replace('user ','')
        return search_users(query,api_key)
    else:
        return search_tracks(inp,api_key)

def search_users(query,api_key=None):
    search_url = soundcloud_url + 'users.json?limit=1&client_id=' + api_key + '&q=' + query.replace(' ','%20')
    print search_url
    result = http.get_json(search_url)
    if not result:
        return 'No users found.'
    result = result[0]

    output = result['username']
    if result['full_name']:
        output += ' (' + result['full_name'] + ')'
    if result['country']:
        output += ' | '
        if result['city']:
            output += result['city'] + ', '
        output += result['country']
    output += ' | ' + str(result['track_count']) + ' tracks, ' + str(result['followers_count']) + ' followers'
    output += ' | ' + result['permalink_url']
    if result['website']:
        output += ' | ' + result['website']
    return output

def search_tracks(query,api_key=None):
    search_url = soundcloud_url + 'tracks.json?limit=1&client_id=' + api_key + '&q=' + query.replace(' ','%20')
    print search_url
    result = http.get_json(search_url)
    if not result:
        return 'No results found.'
    result = result[0]

    output = result['title'] + ', uploaded by ' + result['user']['username'] + ' | Duration: '
    track_length = result['duration'] / 1000
    if track_length < 60:
        output += str(track_length) + 's'
    elif track_length < 3600:
        track_length_s = track_length % 60
        track_length -= track_length_s
        track_length_m = track_length / 60
        output += str(track_length_m) + 'm ' + str(track_length_s) + 's'
    else:
        track_length_s = track_length % 60
        track_length -= track_length_s
        track_length /= 60
        track_length_m = track_length % 60
        track_length -= track_length_m
        track_length_h = track_length / 60
        output += str(track_length_h) + 'h ' + str(track_length_m) + 'm ' + str(track_length_s) + 's'

    plays = "{:,}".format(result['playback_count'])
    output += ' | ' + plays + ' plays | ' + result['permalink_url'] 
    if result['downloadable']:
        output += ' | Downloadable' 
    if result['purchase_url']:
        output += ' | Purchasable at ' + result['purchase_url']
    return output