
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
    if response.error: raise tornado.web.HTTPError(500)
    json = tornado.escape.json_decode(response.body)
    print {"twits": [x['text'] for x in json["results"]]}

clients = []

def broadcast(data):
    for c in clients:
        c.write_message(c)

p = PeriodicCallback(check_twitter, 3000)
#p.start()


class APIWebSocket(websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"
        #clients.append(self)
        self.write_message('waiting')
        self.write_message('waiting')
        self.write_message('waiting')

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        pass

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
