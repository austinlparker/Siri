import requests
from util import hook


@hook.command
def ffstatus(inp, chan=None, say=None):
    servers = requests.get('http://frontier.ffxiv.com/worldStatus/current_status.json').json
    servers_lower = dict((k.lower(), v) for k, v in servers.iteritems())

    if not inp:
        inp = "Excalibur"

    inp_lower = inp.lower()

    try:
        status = int(servers_lower[inp_lower])
        if status != 3:
            return "Server %s is currently \x0309UP\x0f but its still probaly a pile of fucking garbage shit" % inp
        else:
            return "Server %s is currently \x0304DOWN\x0f" % inp
    except:
        return "Unable to find server. Service may also be down."
