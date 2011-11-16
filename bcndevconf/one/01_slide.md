!SLIDE 
# Tornado #

##python async web framework##

 &nbsp;

 @javisantana · bcndevconf 



!SLIDE 
# about me #
* python developer since 2002
* graphics
* @vizzuality // @agroguia

!SLIDE intro 
# index #
* Intro async
* intro tornado
* tornado features
* examples

!SLIDE
# asynchronous
# == 
#HYPE? 

!SLIDE center
#life is evented#
![aldea](async_1.png)

!SLIDE center
#life is evented#
![aldea](async_2.png)

!SLIDE center
#life is evented#
![aldea](async_3.png)

!SLIDE center
#life is evented#
![aldea](async_4.png)

!SLIDE 
#when?#
* handle lots of concurrents 
* websockets/longpoll 
* 'realtime' interaction 
* network applications

!SLIDE
#frameworks#
* nodejs - javascript
* eventmachine - ruby
* twisted, gevent... - python

!SLIDE small
#the basics#

    @@@ python
      OS_register(socket_fd, READ)
      ...
      while True:
          events = OS_get_events() #epoll, select...
          for fd, event_type in events:
            fn = callback_for(fd, event_type)
            fn()

!SLIDE center
#TORNADO#
## **async** web framework ##

!SLIDE center
#others#
- django
- flask
- pylons/pyramid, turbogears ...

!SLIDE center 
#features#
- small · fast · simple
- focus on fundamentals: no models, routes, templates...
- non-blocking I/O

!SLIDE center 
#history#
## friendfeed => facebook ##

!SLIDE center  
#misc#
 - active project on github
![github](tornado_stats.png)
 - **really** good python project example

!SLIDE small
    @@@ python
        import tornado.ioloop
        import tornado.web

        class MainHandler(tornado.web.RequestHandler):
            def get(self):
                self.write("Hello, world")

        application = tornado.web.Application([
            (r"/", MainHandler),
        ])

        if __name__ == "__main__":
            application.listen(8888)
            tornado.ioloop.IOLoop.instance().start()


!SLIDE  commandline

    $ curl -i http://localhost:8888

    HTTP/1.1 200 OK
    Content-Length: 12
    Etag: "e02aa1b106d5c7c6a98def2b13005d5b84fd8dc8"
    Content-Type: text/html; charset=UTF-8
    Server: TornadoServer/2.1.1

    Hello, world

!SLIDE small
#templates

    @@@ python
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.render("index.html", msg="hello!")


!SLIDE commandline

    $ curl -i http://localhost:8888

    HTTP/1.1 200 OK
    Content-Length: 32
    Etag: "3e7020fdb7b87ef428cbdd140c96217044748c27"
    Content-Type: text/html; charset=UTF-8
    Server: TornadoServer/2.1.1

    <html>
    <h1> hello!</h1>
    </html>

!SLIDE small
#json

    @@@ python

    class JSONHandler(tornado.web.RequestHandler):
        def get(self):
            self.write({'msg': "hello!"})

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/json", JSONHandler),
    ])

!SLIDE commandline

    $ curl -i http://localhost:8888/json

    HTTP/1.1 200 OK
    Content-Length: 17
    Etag: "4d34dd0d61eba5957a5ca36846f974697c730a22"
    Content-Type: application/json; charset=UTF-8
    Server: TornadoServer/2.1.1

    {"msg": "hello!"}

!SLIDE bullets
# templates
 - herencia
 - for, if, autoescape...
 - Modules

!SLIDE bullets
# secure cookies 

!SLIDE bullets
# non-blocking requests


!SLIDE end bullets
# fin

##¿preguntas?##

@javisantana
    





