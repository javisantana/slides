
import tornado.ioloop
import tornado.web
import tornado.httpclient

class APIHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://search.twitter.com/search.json?q=bcndevconf",
                   callback=self.async_callback(self.on_response))

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write({"twits": [x['text'] for x in json["results"]]})
        self.finish()

application = tornado.web.Application([
    (r"/api", APIHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
