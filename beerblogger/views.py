# coding: utf-8

from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template, Module

from . import app, pages
from pagination import Pagination  

from models import BlogEntry
from feedformatter import Feed
import locale
 	

''' Template Filters '''
@app.template_filter('dateformat')
def dateformat(value, format=u'%d/%m/%Y'):
    return value.strftime(format)

@app.template_filter('shortmonth')
def shortmonth(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return value.strftime('%B')[:3].upper()

''' Http Errors '''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


BEERS_PER_PAGE = 10

''' Views '''
@app.route('/', defaults={'page': 1})
@app.route('/pagina/<int:page>')
def index(page):
    total_beers = count_all_beers()
    beers = get_beers_for_page(page, BEERS_PER_PAGE,total_beers)
    if not beers:
        abort(404)


    pagination = Pagination(page, BEERS_PER_PAGE, total_beers)
    return render_template('index.html',sorted_entries=beers,
        pagination=pagination)

def get_beers_for_page(page, beers_per_page,total_beers):	
    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(page, beers_per_page)
    return entries

def count_all_beers():	
    count = BlogEntry.select().order_by(('date', 'desc'), ).count()
    return count

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return render_template(template, page=page)


@app.route('/wtf/')
def wtf():
    return render_template('wtf.html')


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
