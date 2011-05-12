# coding: utf-8

from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template, Module

from . import app, pages
from models import BlogEntry
from feedformatter import Feed
import locale

''' Template Filters '''
@app.template_filter('dateformat')
def dateformat(value, format=u'%d/%m/%Y'):
    return value.strftime(format)

@app.template_filter('shortmonth')
def shortmonth(value):
    locale.setlocale(locale.LC_ALL, "pt_BR")
    return value.strftime('%B')[:3].upper()


''' Http Errors '''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


''' Views '''
@app.route('/')
def index():
    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(0, 20)
    return render_template('index.html', sorted_entries=entries)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return render_template(template, page=page)


@app.route('/feed/rss/')
def feed_rss2():
    ENCODING_TAG = '<?xml version="1.0" encoding="UTF-8"?>\n'
    feed_str = make_feed().format_rss2_string()
    return ENCODING_TAG + feed_str


@app.route('/feed/atom/')
def feed_atom():
    return make_feed().format_atom_string()
    
def make_feed():

    feed = Feed()
    
    feed.feed["title"] = app.config['FEED_TITLE']
    feed.feed["link"] = app.config['FEED_LINK']
    feed.feed["author"] = app.config['FEED_AUTHOR']
    feed.feed["description"] = app.config['FEED_DESC']

    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(0, app.config['FEED_ITEMS'])

    for post in entries:
        item = {}

        item["title"] = post.title
        item["link"] = post.link
        item["description"] = post.summary
        
        item["pubDate"] = post.date.utctimetuple()
        item["guid"] = post.eid

        feed.items.append(item)

    return feed