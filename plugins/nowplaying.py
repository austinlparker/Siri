#nowplaying.py
from util import hook, http

api_url = "http://ws.audioscrobbler.com/2.0/?format=json"

@hook.api_key('lastfm')
@hook.command('np')
@hook.command()
def nowplaying(inp,nick='',server='',reply=None,db=None,api_key=None):
    try:
        username, extra = inp.split(' ')
        return ".nowplaying/.np <user> -- lists the currently playing or last played for a Last.fm user"
    except ValueError:
        user = inp

    db.execute("create table if not exists nowplaying(nick primary key, user)")
    newuser = None
    if not user:
        user = db.execute("select user from nowplaying where nick=lower(?)",
                            (nick,)).fetchone()
        if not user:
            user = nick
            newuser = 'TRUE'
        else:
            user = user[0]
      
    print api_url + '&method=user.getrecenttracks&user=' + user + '&api_key=' + api_key
    tracks_json = http.get_json(api_url, method='user.getrecenttracks', user=user, api_key=api_key)
    try: #check if user exists
        return tracks_json['message']
    except:
        pass

    output = user + ' '
    try:
        track = tracks_json['recenttracks']['track'][0]
    except:
        return user + ' has never scrobbled a track.'

    try:
        if track['@attr']['nowplaying']:
            output += 'is now listening to: '
    except:
        output += 'last listened to: '

    artist = track['artist']['#text']
    track_name = track['name']
 
    output += artist + ' - ' + track_name + ' '

    if track['album']['#text']:
        output += '[' + track['album']['#text'] + '] '

    track_info = http.get_json(api_url, method='track.getinfo', track=track_name, artist=artist, username=user, api_key=api_key)
    track_length = int(track_info['track']['duration']) / 1000
    output += '('
    if track_length / 3600:
        output += str(track_length / 3600) + 'h '
    if track_length / 60:
        output += str(track_length / 60) + 'm '
    output += str(track_length % 60) + 's)'
    
    loved = 0
    try:
        plays = track_info['track']['userplaycount']
        loved = track_info['track']['userloved']
    except KeyError:
        output += ' | First play'
        return output
    if plays == '1':
        plays_suffix = ' play'
    else:
        plays_suffix = ' plays'
    if loved == '1':
        plays_suffix += ' | <3'

    output += ' | ' + plays + plays_suffix
    reply(output)

    if inp or newuser:
        db.execute("insert or replace into nowplaying(nick, user) values (?,?)",
                     (nick.lower(), user))
        db.commit()