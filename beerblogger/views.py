# coding: utf-8

from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template, Module

from . import app
from models import BlogEntry

@app.route('/')
def index():
    entries = BlogEntry.select().order_by(('date', 'desc'), ).paginate(0, 20)
    return render_template('index.html', sorted_entries=entries)

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