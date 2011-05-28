===================================
Feed aggregator for beerbloggers !
===================================

What the f*&% is #beerblogging ?
-----------------------------------

It's a f*&%cking bet !




Who are the Beerbloggers ?
-----------------------------------

+ Victor Fontes - http://victorfontes.com/ - http://victorfontes.com/feed/
+ Pedro Marins - http://pedromarins.com/ - http://pedromarins.com/feed/
+ Arlindo Pereira - http://nighto.net/ - http://nighto.net/feed/
+ Tiago Veloso - http://tiagoveloso.com/ - http://tiagoveloso.com/feed/
+ Felipe Arruda - http://www.arruda.blog.br/ - http://www.arruda.blog.br/?feed=rss2
+ Zeno Rocha - http://blog.zenorocha.com/ - http://feeds.feedburner.com/zenorocha
+ Thiago Belem - http://blog.thiagobelem.net/ - http://blog.thiagobelem.net/feed/

If you are beerblogging, add yourself to members.yaml and make a pull request

Let's talk about code ...
-----------------------------------

+ `Python <http://python.org/>`_ programing language
+ `Flask <http://flask.pocoo.org/>`_ microframework for web
+ `Feed Parser <http://www.feedparser.org/>`_ library

Let's install the f*&%cking thing
-----------------------------------
+ To install it, first you need to clone this repository
+ Then install all requirements, using 'beerblogging/beerblogger/etc/requirements.txt'
+ export BEERBLOGGING_SETTINGS to point at your 'beerblogging/beerblogger/setting_dev.py'
+ Run "manage.py create_db" to create the DB
+ Run "manage.py update_entries" to populate the DB
+ Run "manage.py localserver" to run server in localhost:5000

