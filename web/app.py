from flask import Flask, render_template, request, make_response
from flask_sockets import Sockets
from werkzeug.contrib.atom import AtomFeed

import rethinkdb
import redis
import gevent

from listener import IRCLogParser
from websocket import WebsocketBackend


app = Flask(__name__)
sockets = Sockets(app)

app.config.from_object('config')

logger = IRCLogParser()

rethinkdb.connect('localhost', 28015).repl()
log_db = rethinkdb.db('siri').table('logs')
url_db = rethinkdb.db('siri').table('urls')
red = redis.Redis()

chatsocket = WebsocketBackend('irc_chat')
chatsocket.start()

urlsocket = WebsocketBackend('irc_urls')
urlsocket.start()


@app.route('/')
def index():
    active_channels = list(red.smembers('irc_channels'))
    all_channels = [chan['channel'] for chan in log_db.pluck('channel').distinct().run()]
    return render_template("index.html", active=active_channels, all_chans=all_channels)


@app.route('/grid/<channel>')
def channel_images(channel):
    urls = list(url_db.filter({'channel': channel}).run())[:50]
    return render_template("grid.html", channel=channel, urls=urls)


@app.route('/links/<channel>')
def channel_urls(channel):
    pass


@app.route('/rss/<channel>.atom')
def rss(channel):
    urls = list(url_db.filter({'channel': channel}).run())[:50]
    feed = AtomFeed('Recent URLs', feed_url=request.url, url=request.url_root)
    for url in urls:
        feed.add(url['title'], "This URL is a {0}".format(url['type']),
                 content_type="html",
                 author=url['user'],
                 url=url['url'],
                 updated=url['timestamp'],
                 published=url['timestamp'])
    data = feed.get_response()
    response = make_response(data)
    response.headers['Content-Type'] = 'application/atom+xml'
    return response


@sockets.route('/chat')
def chat_socket(ws):
    chatsocket.register(ws)

    while ws.socket is not None:
        gevent.sleep()


@sockets.route('/urls')
def url_socket(ws):
    urlsocket.register(ws)

    while ws.socket is not None:
        gevent.sleep()
