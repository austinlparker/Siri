import json
import time

import redis

from util import hook


@hook.api_key('web')
@hook.regex('.*')
def chat_log(match, nick=None, chan=None, bot=None, conn=None, api_key=None):
    r = redis.Redis(host=api_key['redis']['address'],
                    port=api_key['redis']['port'],
                    db=api_key['redis']['db'])
    message = {
        "bot": conn.nick,
        "user": nick,
        "channel": chan.replace("#", ""),
        "content": match.group(),
        "server": conn.server,
        "timestamp": str(int(time.time()))
    }
    r.publish('chat', json.dumps(message))


@hook.api_key('web')
@hook.regex('.*')
def update_channels(match, conn=None, api_key=None, chan=None):
    r = redis.Redis(host=api_key['redis']['address'],
                    port=api_key['redis']['port'],
                    db=api_key['redis']['db'])

    chan = chan.replace("#", "")
    if not r.exists('irc_channels'):
        r.sadd('irc_channels', chan)
        r.expire('irc_channels', 300)
    else:
        r.sadd('irc_channels', chan)
