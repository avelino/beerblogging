# -*- coding: utf-8 -*-
"""
    beerblogging
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from flask import Flask, g, render_template, request

from flaskext.gravatar import Gravatar
from flaskext.sqlalchemy import SQLAlchemy
from paginator import Paginator

from helpers import to_html, br_month_filter

app = Flask(__name__)
app.config.from_object('beerapp.settings')

db = SQLAlchemy(app)
gravatar = Gravatar(
    app,
    size=75,
    rating='x',
    default='retro',
    force_default=False,
    force_lower=False)

paginator = Paginator(app)

from members import Members
members = Members(app)

app.jinja_env.filters['br_month'] = br_month_filter

from posts import *

paginator.register('posts', BlogPost.query.count)

from feed_generator import FeedGenerator


def TAGS():
    _TAGS = []
    for b in BlogPost.query.group_by(BlogPost.author_email):
        if b.tags != "":
            for tag in b.tags.split(","):
                _TAGS.append(tag.strip())
    return set(_TAGS)


@app.route('/')
@app.route('/tag/<tag>')
@to_html('index.html')
def index(tag=None):
    pagination = paginator.for_posts
    posts = BlogPost.latest_posts()
    if tag:
        posts = posts.filter(BlogPost.tags.like('%{0}%'.format(tag)))
    latest_posts = posts.paginate(
        pagination.page, pagination.per_page).items

    tags = TAGS()
    return locals()


@app.route('/wtf/')
def wtf():
    return render_template('wtf.html', tags=TAGS())


@app.route('/feed/<feed_fmt>/')
def teste(feed_fmt):
    feed_bb = FeedGenerator(
        title=app.config['FEED_TITLE'],
        link=app.config['FEED_LINK'],
        author=app.config['FEED_AUTHOR'],
        description=app.config['FEED_DESC'])
    feed_posts = BlogPost.latest_posts().paginate(
        1, app.config['FEED_ITEMS']).items

    for p in feed_posts:
        feed_bb.add_item(p.title, p.link, p.excerpt, p.date_updated, p.id_post)

    if feed_fmt.lower() == 'atom':
        return feed_bb.atom()
    else:
        return feed_bb.rss()
