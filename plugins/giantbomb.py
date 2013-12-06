from util import hook, http

giantbomb_search_api = 'http://www.giantbomb.com/api/search/?format=json&api_key='
search_types = ('game', 'franchise', 'character', 'concept', 'object', 'location', 'person', 'company', 'video')
reviewer_surname = {
    "Jeff":"Gerstmann",
    "Ryan":"Davis",
    "Brad":"Shoemaker",
    "Vinny":"Caravella",
    "Dave":"Snider",
    "Alex":"Navarro",
    "Drew":"Scanlon",
    "Andy":"McCurdy",
    "Matt":"Kessler",
    "Patrick":"Klepek"}

@hook.api_key('giantbomb')
@hook.command('gb')
@hook.command()
def giantbomb(inp,api_key=None):
    ".giantbomb/.gb [game|franchise|character|concept|object|location|person|company|video] <query>"\
    " -- return the first result of a Giant Bomb search"
    
    try: #check for a valid search type in first param 
        type, query = inp.split(' ', 1)
        if type not in search_types: #if it's not there then search in any category
            raise ValueError
    except ValueError: #if single word paramater
        type = ''
        query = inp

    query = query.replace(' ','%20') #format search query

    if type: #add the content type to the search if there is one
       type = '&resources=' + type

    search_url = giantbomb_search_api + api_key + '&query=' + '\"' + query + '\"' + type
    results = http.get_json(search_url)

    if results['number_of_total_results'] == 0:
       return 'No results found'

    top_result = results['results'][0] 
    page_url = top_result['site_detail_url']

    video_subscriber = ''
    if top_result['resource_type'] == 'video':
        if top_result['video_type'] == 'Trailers': #preference other content over trailers cause they suck
            for i in range(1,results['number_of_page_results']): #keep going until we view all video results
                curr_result = results['results'][i]
                if curr_result['video_type'] != 'Trailers': #get the first non-trailer
                    top_result = curr_result
                    page_url = top_result['site_detail_url']
                    break
        if top_result['video_type'] == 'Subscriber': #if subscriber only video then tag it as such
            video_subscriber = '[Subscriber] '
        elif top_result['youtube_id']: #if there is a youtube video, link that alongside the giant bomb page
            page_url += ' | http://youtube.com/watch?v=' + top_result['youtube_id']

    #get page deck (brief description)
    page_api_url = top_result['api_detail_url'] + '?format=json&api_key=' + api_key
    result_object = http.get_json(page_api_url)['results']
    deck = ''
    if result_object['deck']: #if the page has no deck don't display it!
       deck = ' | ' + result_object['deck']

    #if result is a game then get a review if one exists
    if top_result['resource_type'] == 'game':
        try:
            review_api_url = result_object['reviews'][0]['api_detail_url'] + '?format=json&api_key=' + api_key
            review_object = http.get_json(review_api_url)['results']
            reviewer = review_object['reviewer']
            score = str(review_object['score'])
            deck += ' | ' + score + '/5 Stars from ' + reviewer + ' ' + reviewer_surname[reviewer]
        except KeyError: #the reviews object won't exist if there are no reviews
            pass

    return video_subscriber + page_url + deck
