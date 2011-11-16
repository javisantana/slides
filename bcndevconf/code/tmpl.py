
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", msg="hello!")

class JSONHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({'msg': "hello!"})

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/json", JSONHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
