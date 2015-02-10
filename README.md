# BeerBlogging

[![Build Status](https://travis-ci.org/avelino/beerblogging.svg?branch=master)](https://travis-ci.org/avelino/beerblogging)

[![Coverage Status](https://coveralls.io/repos/avelino/beerblogging/badge.svg)](https://coveralls.io/r/avelino/beerblogging)

## What the f*&% is #beerblogging ?

It's a f*&%cking bet!

You have 1 month to write at least 1 blogpost. If you don't do that, you have to pay a beer for everybody.

## Who are the BeerBloggers ?

* Daniel Filho: [Blog](http://danielfilho.github.io) ~ [Feed](http://danielfilho.github.io/feed.xml)
* Felipe Arruda: [Blog](http://arruda.blog.br/) ~ [Feed](http://www.arruda.blog.br/?feed=rss2)
* Renato Mangini: [Blog](http://www.renatomangini.com/) ~ [Feed](http://www.renatomangini.com/feeds/posts/default)
* Thiago Avelino: [Blog](http://avelino.us/) ~ [Feed](http://feeds.feedburner.com/pyavelino)
* Zeno Rocha: [Blog](http://zenorocha.com/) ~ [Feed](http://feeds.feedburner.com/zenorocha)
* Ellison Leão: [Blog](https://medium.com/@ellisonleao) ~ [Feed](https://medium.com/feed/@ellisonleao)
* Eric Hideki:[Blog](http://ericstk.wordpress.com) ~ [Feed](https://ericstk.wordpress.com/feed/)
* Mateus Ortiz: [Blog](http://mateusortiz.com) ~ [Feed](http://feeds.feedburner.com/mateusortiz)

## Let's talk about code...

We're using:

* [Python](http://python.org/) programing language
* [Flask](http://flask.pocoo.org/) microframework for web
* [Feed Parser](http://www.feedparser.org/) library

## Install

1. First you need to clone this repository: `git clone git@github.com:avelino/beerblogging.git`
* Then install all requirements by running `pip install -r requirements.txt`
* Run `./manager.py create_db` to create the database
* Run `./manager.py fetch_posts` to populate the database
* Run `./manager.py run` to run server in [localhost:5000](http://localhost:5000)


## Testing

Just execute:

```
$ make test
```

And it should run the tests for you.

## Deploying

To deploy on Heroku:

* `heroku create`
* `heroku addons:add heroku-postgresql:dev`
* `heroku pg:promote HEROKU_POSTGRESQL_COLOR_URL`
* `git push heroku master`
* `heroku run python manager.py create_db`
* `heroku run ./update_posts.sh`

**OBS:** The `update_posts.sh` should be runned everytime, to keep tracking new posts.
