from util import hook, http
import random

api_url = "http://ws.audioscrobbler.com/2.0/?format=json"

@hook.api_key('lastfm')
@hook.command(autohelp=False)
def lastfm(inp,nick=None,api_key=None):
    ".lastfm [user1] [user2] -- gets Last.fm information about a single user or compares two users. "\
    "If user1 is blank then the user matching the current nickname will be returned."

    try:
        user1, user2 = inp.split(' ')
        return compare(user1,user2,api_key)
    except ValueError:
        user = inp
    if not inp:
        user = nick

    user_json = http.get_json(api_url, method='user.getinfo', user=user, api_key=api_key)
    try: #check if user exists
        return user_json['message'].replace('that name','the name ' + user)
    except:
        pass

    user_info = user_json['user']
    output = user_info['url'] + ' | ' + user_info['playcount'] + ' plays'
    if user_info['playcount'] != '0': #keyerror with zero plays
        output += ' | Top artists: '
        top_artists = http.get_json(api_url, method='user.gettopartists', user=user, api_key=api_key)['topartists']
        count = int(top_artists['@attr']['total'])
        top_artists = top_artists['artist']
        if count == 0: #arnie is a dick and had only two artists and tracks
            output += 'none'
        elif count > 4:
            count = 3
        print count
        for i in range(0,count):
            output += top_artists[i]['name'] + ' (' + top_artists[i]['playcount'] + ')'
            if i < (count-1):
                output += ', '

        output += ' | Top tracks: '
        top_tracks = http.get_json(api_url, method='user.gettoptracks', user=user, api_key=api_key)['toptracks']
        count = int(top_tracks['@attr']['total'])
        top_tracks = top_tracks['track']
        if count == 0:
            output += 'none'
        elif count > 4:
            count = 3
        print count
        for i in range(0,count):
            output += top_tracks[i]['artist']['name'] + ' - ' + top_tracks[i]['name'] + ' (' + top_tracks[i]['playcount'] + ')'
            if i < (count-1):
                output += ', '

    return output

def compare(user1,user2,api_key,bound=None):
    comparison = http.get_json(api_url, method='tasteometer.compare', type1='user', type2='user', value1=user1, value2=user2, limit='100', api_key=api_key)
    try: #check if user exists
        return comparison['message']
    except: #will throw keyerror if user exists
        pass
    
    comparison = comparison['comparison']['result']
    score = float(comparison['score']) * 100
    score = str(score)
    score = score[:5] # get first four digits
    output = user1 + ' and ' + user2 + ' are ' + score + '%' + ' compatible. | Mutual artists: '

    try:
        if comparison['artists']['@attr']:
            matches = int(comparison['artists']['@attr']['matches'])
            if matches < 5: #get up to five mutual artists
                bound = matches
            else:
                bound = 5
    except: #if no mutual artists then matches attr doesn't exist
       pass

    if not bound:
        output += 'none'
    else:
        intlist = ''
        for i in range(0,bound): 
            randartist = random.randint(0,(matches-1))
            while str(randartist) in intlist: #keep getting artists until
                randartist = random.randint(0,(matches-1))
            output += comparison['artists']['artist'][randartist]['name']
            intlist += str(randartist)
            if i < (bound - 1):
                output += ', '

    return output
