from util import hook, http
leafly_url = 'http://leafly.com/api/details/'

@hook.command('weed')
@hook.command
def leafly(inp):
       '.leafly/.weed <strain> -- gets weed strain data from Leafly.com'
       inp_key = inp.replace(' ', '-').lower() #leafly api key is in lower case with hyphens for spaces
       full_url = leafly_url + inp_key

       results = http.get_json(full_url)
       try:
           print results['Key'] #check if we got a json object
       except KeyError:
           return inp + ' not found on Leafly.com'

       #formatting the output
       fulloutput = 'Strain: ' + results['Name']
       fulloutput += ' | ' + results['Category']
       fulloutput += ' | Rating: ' + str(results['Rating'])
       fulloutput += ' | ' + results['Abstract']

       fulloutput += ' | Feelings:' + listtopthree(results['Effects'])
       fulloutput += ' | Negatives:' + listtopthree(results['Negative'])
       fulloutput += ' | Medical uses:' + listtopthree(results['Medical'])

       fulloutput += ' | ' + results['Url']

       return fulloutput

def listtopthree(results): #get top three effects/negatives/medical uses
       out = ''
       for i in range(0,3):
          topcurrent = results[i]
          out += ' ' + topcurrent['Name']
          if i is not 2: #comma separate the first two
              out += ','
       return out
