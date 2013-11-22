from util import hook, http
goatkcd_url = 'http://goatkcd.com/'

@hook.command('xkcd')
@hook.command
def goatkcd(inp):
    key = inp
    strips = 'strips'
    nsfw_tag = '(NSFW) '

    if inp.endswith("sfw"):
        key = key[:-4].strip()
        strips += '_sfw' #change url used from /strips to /strips_sfw
        nsfw_tag = '' #remove nsfw tag

    if not key: #if no comic number specified get random
	    key = 'random'
    elif key.isalpha(): #in a valid command, should be no characters
           return '.goatkcd/.xkcd [#] [sfw] -- returns a goatkcd comic with specified number (if exists), random otherwise.'  

    if key != 'random': #check to make sure random comic actually exists
        try:
            http.open(goatkcd_url + strips + key + '.jpg').getcode() #check if given comic number actually exists
        except http.HTTPError:
            key = 'random' #if it doesn't then just use random

    base_url = http.open(goatkcd_url + key).geturl() #to get the comic number for randoms
    img_id = base_url.strip(goatkcd_url) #get just the comic number
    img_url = goatkcd_url + strips + '/' + img_id + '.jpg' #combine them all together to form the full url

    return nsfw_tag + img_url
