import json

from flask import Flask, render_template
from flask_sockets import Sockets

import rethinkdb
import redis

from listener import IRCLogParser


app = Flask(__name__)
sockets = Sockets(app)

app.config.from_object('config')

logger = IRCLogParser()

rethinkdb.connect('localhost', 28015).repl()
log_db = rethinkdb.db('siri').table('logs')
url_db = rethinkdb.db('siri').table('urls')
red = redis.Redis()


@app.route('/')
def index():
    active_channels = list(red.smembers('irc_channels'))
    all_channels = [chan['channel'] for chan in log_db.pluck('channel').distinct().run()]
    return render_template("index.html", active=active_channels, all_chans=all_channels)


@app.route('/grid/<channel>')
def channel_images(channel):
    urls = list(url_db.filter({'channel': channel}).run())
    return render_template("grid.html", channel=channel, urls=urls)


@app.route('/links/<channel>')
def channel_urls(channel):
    pass


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)
