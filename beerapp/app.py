# -*- coding: utf-8 -*-
"""
    beerblogging
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import yaml
from flask import Flask, render_template

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

from posts import BlogPost

paginator.register('posts', BlogPost.query.count)

from feed_generator import FeedGenerator


def TAGS():
    _TAGS = []
    members_str = open(app.config['MEMBERS_FILE']).read()
    for member in yaml.load_all(members_str):
        if member.get('tags'):
            for tag in member['tags'].split(","):
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
