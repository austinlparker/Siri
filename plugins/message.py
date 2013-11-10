from util import hook
import rethinkdb


rdb_conn = rethinkdb.connect('localhost', 28015)
log_db = rethinkdb.db('siri').table('logs')
all_channels = [chan['channel'] for chan in log_db.pluck('channel').distinct().run(rdb_conn)]

@hook.command
def message_all(inp, chan=None, conn=None, nick=None):
    chans = ["#" + channel for channel in all_channels]
    admins = ['elgruntox']
    
    if nick.lower() not in admins:
        return "Acess Denied"
    
    for chan in chans:
        conn.msg(chan, inp)

    print "Message sent to " + ", ".join(chans)

