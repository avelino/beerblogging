# coding: utf-8

from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template, Module

from . import app
from models import BlogEntry
from feedformatter import Feed

''' Template Filters '''
@app.template_filter('dateformat')
def dateformat(value, format=u'%d/%m/%Y'):
    return value.strftime(format)


@app.template_filter('timeformat')
def timeformat(value, format=u'%H:%M'):
    return value.strftime(format)


''' Http Errors '''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


''' Views '''
@app.route('/')
def index():
    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(0, 20)
    return render_template('index.html', sorted_entries=entries)

@app.route('/feed/rss/')
def feed_rss2():
    return make_feed().format_rss2_string()


@app.route('/feed/atom/')
def feed_atom():
    return make_feed().format_atom_string()
    
def make_feed():
    FEED_TITLE = "BeerBlogging"
    FEED_LINK = "http://www.beerblogging.net"
    FEED_AUTHOR = "BeerBloggin Team"
    FEED_DESC = "Beerblogging Feed"
    FEED_ITEMS = 20

    feed = Feed()

    # Set the feed/channel level properties
    feed.feed["title"] = FEED_TITLE
    feed.feed["link"] = FEED_LINK
    feed.feed["author"] = FEED_AUTHOR
    feed.feed["description"] = FEED_DESC

    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(0, FEED_ITEMS)

    for post in entries:
        item = {}

        item["title"] = post.title
        item["link"] = post.link
        item["description"] = post.summary
        
        item["pubDate"] = post.date.utctimetuple()
        item["guid"] = post.eid

        feed.items.append(item)

        return feed