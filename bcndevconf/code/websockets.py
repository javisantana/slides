
import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.ioloop import PeriodicCallback
from tornado import websocket

def check_twitter(s='bcndevcon'):
    http = tornado.httpclient.AsyncHTTPClient()
    http.fetch("http://search.twitter.com/search.json?q=" + s,
               callback=new_twitts)

def new_twitts(response):
    if not response.error: 
        json = tornado.escape.json_decode(response.body)
        data = {"twits": [x['text'] for x in json["results"]]}
        broadcast(data)

clients = []

def broadcast(data):
    for c in clients:
        c.write_message(data)

p = PeriodicCallback(check_twitter, 3000)
p.start()


class APIWebSocket(websocket.WebSocketHandler):
    def open(self):
        clients.append(self)

    def on_message(self, message):
        print message

    def on_close(self):
        print "client diconnected"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("websocket.html")

application = tornado.web.Application([
    (r"/api", APIWebSocket),
    (r"/", MainHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
