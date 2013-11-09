import redis
import gevent


redis = redis.Redis()

class WebsocketBackend(object):
    def __init__(self, rchan):
        self.clients = []
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(rchan)

    def data_loop(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                print data
                yield data

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        for data in self.data_loop():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)
