import json
import re
import urlparse
import datetime
import calendar

import redis
import rethinkdb
import requests
import lxml.html

import gevent
from gevent import monkey
monkey.patch_all()



def json_datetime(obj):
    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    utc = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
    return utc


url_re = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class IRCLogParser(object):
    def __init__(self, chan="chat", host="localhost", port=6379, db=0):
        self.chan = chan
        self.red = redis.Redis(host=host, port=port, db=db)

        pubsub = self.red.pubsub()
        gevent.spawn(self.sub, pubsub)

    def sub(self, pubsub):
        pubsub.subscribe(self.chan)
        for message in pubsub.listen():
            if type(message['data']) is str:
                gevent.spawn(self.parse_message, message)
            else:
                pass

    def parse_message(self, message):
        message = json.loads(message['data'])
        rethinkdb.connect('localhost', 28015).repl()
        log_db = rethinkdb.db('siri').table('logs')

        data = {
            'channel': message['channel'],
            'timestamp': rethinkdb.now(),
            'user': message['user'],
            'content': message['content'],
            'server': message['server'],
            'bot': message['bot']
        }

        log_db.insert(data).run()

        urls = re.findall(url_re, message['content'])
        if urls:
            for url in urls:
                urldata = {
                    'url': url,
                    'user': message['user'],
                    'channel': message['channel'],
                    'server': message['server'],
                    'bot': message['bot'],
                    'timestamp': rethinkdb.now()
                }
                gevent.spawn(self.parse_url, urldata)

        data['timestamp'] = datetime.datetime.utcnow()
        self.red.publish('irc_chat', json.dumps(data, default=json_datetime))

    def parse_url(self, urldata):
        print 'GOT URL: %s' % urldata
        allowed_types = ['text', 'audio', 'image']
        video_hosts = ['www.youtube.com', 'youtube.com', 'vimeo.com', 'www.vimeo.com', 'youtu.be']
        
        r = requests.get(urldata['url'], timeout=5)
        if r.status_code == 200:
            content_type = r.headers['content-type'].split('/')[0]
            
            if content_type not in allowed_types:
                return None
            
            if content_type == 'text':
                parse = urlparse.urlparse(urldata['url'])
                if parse.hostname in video_hosts:
                    urldata['type'] = 'video'
                else:
                    urldata['type'] = 'website'

                try:
                    urldata['title'] = lxml.html.parse(urldata['url']).find(".//title").text
                except:
                    urldata['title'] = "No Title"
                
            else:
                urldata['title'] = content_type.title()
                urldata['type'] = content_type

            rethinkdb.connect('localhost', 28015).repl()
            url_db = rethinkdb.db('siri').table('urls')
            url_db.insert(urldata).run()

            urldata['timestamp'] = datetime.datetime.utcnow()
            self.red.publish('irc_urls', json.dumps(urldata, default=json_datetime))
