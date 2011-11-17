!SLIDE 
# Tornado #

##python async web framework##

 &nbsp;

 @javisantana · bcndevcon


!SLIDE 
# about me #
* python developer since 2002
* @vizzuality // @agroguia

!SLIDE intro 
# index #
* intro async
* intro tornado
* tornado features (by example)
* production 

!SLIDE corte center
# **asynchronous**
# == 
#**HYPE**? 

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

!SLIDE center corte
#TORNADO#
## **async** web framework ##

!SLIDE center
#others#
- django
- flask
- pylons/pyramid, turbogears ...

!SLIDE center
#sorry, **no benchmarks**#

!SLIDE center 
#overview#
- small · fast · simple
- focus on fundamentals: no models, routes, templates...
- non-blocking I/O

!SLIDE center 
#history#
## friendfeed => facebook ##

!SLIDE center 
#fist step, hello world

!SLIDE small
    @@@ python
        import tornado.ioloop
        import tornado.web

        # controller
        class MainHandler(tornado.web.RequestHandler):
            def get(self):
                self.write("Hello, world")

        # router + settings
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

!SLIDE corte center
#features#


!SLIDE small
#templates

    @@@ html 
        <!-- index.html -->
        <html>
            <h1>{{msg}}</h1>
        </html>

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

!SLIDE  small
# templates
 - inherance 
 - for, if, autoescape...
 - Modules
 - **no limits**, just python code

        @@@ html 
        {% for student in 
            [p for p in people 
                if p.student and p.age > 23] %}
          <li>{{ epic_function(student.name) }}</li>
        {% end %}

!SLIDE  small
# async code 
## external http service example

!SLIDE smaller

    @@@ python

    SEARCH = "http://search.twitter.com/search.json?q=bcndevcon"
    class APIHandler(tornado.web.RequestHandler):

        @tornado.web.asynchronous
        def get(self):
          http = tornado.httpclient.AsyncHTTPClient()
          http.fetch(SEARCH,
            callback=self.async_callback(
                self.on_response # <== call here when done
            )
          )

        def on_response(self, response): # <== HERE!
            json = tornado.escape.json_decode(response.body)
            self.write({
              "twits": [x['text'] for x in json["results"]]
            })
            self.finish()

!SLIDE commandline small
    $ curl http://localhost:8888/api | python -m json.tool

    {
        "twits": [
            "Llegando a la. #bcndevconf A conocer a Lucia @wiseri :-)", 
            "De camino a #bcndevconf. Tres d\u00edas de congreso en el museo mar\u00edtimo de barcelona. A ver q tal", 
            "On my way to BCN with @davideme and tomorrow BCNDevConf!", 
            "@wulczer vas a estar t\u00fa en la bcndevconf hablando de ducksboard?", 
            "In extremis, per\u00f2 l'equip de @shopsial acaba de comprar els early tickets per el #bcndevconf Ens veiem all\u00e0 la setmana que ve!!", 
            "@ValentiGoClimb @bcndevconf see you there!", 
            "+1 RT @ValentiGoClimb: i will be in @bcndevconf on Saturday 19! #bdc11", 
            "i will be in @bcndevconf on Saturday 19! #bdc11"
        ]
    }

!SLIDE bullets
# websockets

!SLIDE smaller 
    @@@ javascript 
    // websocket.html
    window.onload = function() {

        var WS = typeof WebSocket === 'function' ? WebSocket : MozWebSocket;
        var ws = new WS("ws://localhost:8888/api");

        ws.onopen = function() {
           ws.send("Hello");
        };

        ws.onmessage = function (evt) {
           var h = "<h1>" + new Date().toString() + "</h1>";
           h += "<ul>";
           JSON.parse(evt.data).twits.forEach(function(r) {
              h += "<li>" + r;
           });
           h += "</ul>";
           document.body.innerHTML = h;
        };
    }

!SLIDE smaller
    @@@ python
    # websocket handler
    # clients
    clients = [] #<= 1 thread!

    class APIWebSocket(websocket.WebSocketHandler):
        def open(self):
            clients.append(self) # <= add the client to the list

        def on_message(self, message):
            print message

        def on_close(self):
            print "client diconnected"
            #TODO: remove the client from clients list

    # route
    application = tornado.web.Application([
        (r"/api", APIWebSocket),
    ])

!SLIDE smaller
    @@@ python
    # get tweets task
    def check_twitter(s='bcndevcon'):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://search.twitter.com/search.json?q=" + s,
                   callback=new_twitts) #<= callback

    # setup a periodic task
    p = PeriodicCallback(check_twitter, 3000)
    p.start()

    # callback for twitter search 
    def new_twitts(response):
        json = tornado.escape.json_decode(response.body)
        data = {"twits": [x['text'] for x in json["results"]]}
        broadcast(data) # <= broadcast to all clients


    def broadcast(data):
        for c in clients:
            c.write_message(data) #<= write to websockets


!SLIDE 
#socket.io#
## tornadio2 ##


!SLIDE
# more
- secure cookies
- mysql database helper (sync)
- oauth/twitter/gooogle/facebook mixins
- twisted connector
- decorators: auth, **gen**
- process management
- python3!

!SLIDE
# the bad
- expection handling (solved in 2.x) 
- no ORM, forms, session...
- no dev tools (middleware...)


!SLIDE corte center
#production#

!SLIDE 
#when#
- API
- connectors
- fast/realtime stuff

!SLIDE  small
#when **not** to use#
- as general framework
- no ORM
- no forms handling
- no general 3rd party plugins
- 3rd party plugins => **broken** => be careful

!SLIDE 
#setup#
 - behind a proxy (nginx)
 - websockets 
    - HTTP 1.1 proxy
    - tornado => port XXXX
 - workers + redis

!SLIDE small
#nginx#
    @@@ sh
    # simplified config
    http {
        upstream frontends {
            server 127.0.0.1:8000;
        }
        server {
            location ^~ /static/ {
                root /home/www/app/static;
                if ($query_string) { expires max; }
            }
            location / {
                proxy_pass http://frontends;
            }
        }
    }

!SLIDE smaller
#supervisor#
    @@@ sh
    [program:tornado]
    command=/home/www/app/env/bin/python /home/www/app/src/app.py
    directory=/home/www/app/
    user=no_root;

!SLIDE corte center
#final thoughts#

!SLIDE 
## simple
## fast
## no silver bullet
## good python project
## micro framework

!SLIDE end bullets
# fin

##¿Questions?##

@javisantana

!SLIDE 
# refs
* http://www.tornadoweb.org/
* http://bret.appspot.com/entry/tornado-web-server
* tornado code on github






