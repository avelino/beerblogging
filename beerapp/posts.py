# -*- coding: utf-8 -*-

from app import db, members

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.String(128), nullable=True)

    author_email = db.Column(db.String(128))
    group_name = db.Column(db.String(120), nullable=True)

    title = db.Column(db.String(256))
    link = db.Column(db.String(512), unique=True)

    excerpt = db.Column(db.Text, default='')
    content = db.Column(db.Text, default='')

    date_post = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)

    tags = db.Column(db.String(512), default='')  

    beers = db.Column(db.Integer,default=0)

    def __init__(self, email, title, link, id_post, date_post, date_updated, excerpt='', content='', tags='',beers=0):
        self.author_email = email

        self.title = title
        self.link = link
        self.id_post = id_post

        self.date_post = date_post
        self.date_updated = date_updated

        self.excerpt = excerpt
        self.content = content
        self.tags = tags
        self.beers = beers

    @hybrid_property
    def member(self):
        return members.for_email(self.author_email)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def __repr__(self):
        return '<Post %s de %s>' % (self.id_post, self.author_email)

    @classmethod
    def latest_posts(cls):
        return cls.query.order_by(cls.date_updated.desc())