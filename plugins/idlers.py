from util import hook
import time
import requests
from datetime import timedelta, datetime


getting_names = False
users = []

@hook.event('353')
def names_hook(event, input=None, conn=None, chan=None, nick=None):
    global getting_names
    global users

    if not getting_names:
        getting_names = True
        users = []

    if chan[0] != '#':
        chan = event[2]

    if chan != "#yospos":
        return

    users_raw = event[3].strip().split(' ')
    for user in users_raw:
        if user[0] in ['+', '%', '@', '&', '~']:
            user = user[1:]
        users.append(user)

 
@hook.event('366')
def end_names_hook(event, input=None, conn=None, chan=None, nick=None):
    getting_names = False


@hook.command
def idlecaust(inp, say=None, chan=None, nick=None, db=None, conn=None):
    global users
    admins = ['elgruntox', 'jonny290', 'sniep']
    chans = ['#yospos']
    whitelist = ['tef', 'sl^^', 'rocketsauce']

    kick = False

    if chan not in chans:
        return 'Access Denied. Admins are ' + ' '.join(admins)

    e = conn.cmd('NAMES', [chan])
    arg1 = inp.split(' ')[0]

    days = 7

    if arg1 == 'kick':
        if nick not in admins:
            return 'Access Denied. Admins are ' + ', '.join(admins)
        else:
            kick = True
            try:
                kick_message = inp.split(' ')[1]
            except IndexError:
                kick_message = 'Peace out bro.'
        
    elif arg1 == 'ban':
        if nick not in admins:
            return 'Access Denied. Admins are ' + ', '.join(admins)
        return 'TODO'

    else:
        try:
            days = int(inp.split(' ')[0])
            if days < 7:
                days = 7
        except IndexError:
            days = 7

    time.sleep(2)
    offset = datetime.utcnow() - timedelta(days=days)   
    time_check = time.mktime(offset.utctimetuple())

    idlers_q = set(db.execute("select name, time from seen where chan='#yospos' and CAST(time as integer)<CAST(? as integer)", (time_check,)))
    #print idlers_q
    idlers = [idler[0] for idler in idlers_q]
    results_1 = [x for x in idlers if x in users]
    results = [x for x in results_1 if x not in whitelist]

    if kick:
        say('[!] KICKING IDLERS [!] - BEEP - BEEP - [!] KICKING IDLERS [!]')
        for user in results:
            conn.cmd('MODE', ['#yospos', '+b', user])
            conn.cmd('KICK', ['#yospos', user, kick_message])
            time.sleep(2)
            conn.cmd('MODE', ['#yospos', '-b', user+'!*@*'])
            conn.cmd
        users = []
        return('CRISIS OVER THE KICK IS COMPLETE')
    
    users = []
    return "These fuckers havent talked in {0} days: {1}".format(days, ", ".join(results))
