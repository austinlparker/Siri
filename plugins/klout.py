import requests
from util import hook


@hook.command
def klout(inp, chan=None, say=None):
    """Returns the klout score of the specified twitter user"""

    id_url = 'http://api.klout.com/v2/identity.json/twitter?screenName=' + inp + '&key=bg2smqgwxra6uhpx6dd9xuke'
    kid = requests.get(id_url).json()
    if kid.get('id', None):
        score_url = 'http://api.klout.com/v2/user.json/' + kid['id'] + '/score?key=' + 'bg2smqgwxra6uhpx6dd9xuke'
        topic_url = 'http://api.klout.com/v2/user.json/' + kid['id'] + '/topics?key=bg2smqgwxra6uhpx6dd9xuke'
        topics_list = requests.get(topic_url).json()
        score = int(requests.get(score_url).json()['score'])
        topics = ', '.join([x['displayName'] for x in topics_list][0:5])
        influenced = requests.get('http://api.klout.com/v2/user.json/' + kid['id'] + '/influence?key=bg2smqgwxra6uhpx6dd9xuke').json()
        inf = influenced['myInfluencers'][0]['entity']['payload']

        return "%s's Score: %s | Last influenced by: %s (%.2f) | Known For: %s" % (inp, score, inf['nick'], inf['scoreDeltas']['dayChange'], topics)
    else:
        return "Unable to find a klout score for that twitter user."
