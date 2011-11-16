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
# asynchronous == HYPE? #

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




!SLIDE end bullets
# fin

##¿preguntas?##

@javisantana
    





