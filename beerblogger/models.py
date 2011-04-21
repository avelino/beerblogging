#coding: utf-8
import peewee
DATABASE_NAME = '/deploy/beerblogging/beerblogger/db.sqlite'
database = peewee.Database(peewee.SqliteAdapter(), DATABASE_NAME)
from members import *

# ['updated', 'slash_comments', 'updated_parsed', 'links', '', 'author', 'summary_detail', 'comments', '', '', 'guidislink', 'title_detail', 'link', 'authors', 'author_detail', 'wfw_commentrss', 'id', 'tags'] #}
# model definitions

class BlogEntry(peewee.Model):
    title =     peewee.CharField()
    eid =       peewee.CharField()
    link =      peewee.CharField()

    author_email = peewee.CharField()

    summary =   peewee.TextField() 
    tags =      peewee.CharField()
    content =   peewee.TextField()

    date =      peewee.DateTimeField()
    updated =   peewee.DateTimeField()
    
    class Meta:
        database = database

    @property
    def author(self):
        return Members().by_email(self.author_email)

    '''
    class member
    def following(self):
        return User.select().join(
            Relationship, on='to_user_id'
        ).where(from_user=self).order_by('username')

    def followers(self):
        return User.select().join(
            Relationship
        ).where(to_user=self).order_by('username')

    def is_following(self, user):
        return Relationship.select().where(
            from_user=self,
            to_user=user
        ).count() > 0

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)


class Relationship(peewee.Model):
    from_user = peewee.ForeignKeyField(User, related_name='relationships')
    to_user = peewee.ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = database


class Entry(peewee.Model):
    user = peewee.ForeignKeyField(User)
    content = peewee.TextField()
    pub_date = peewee.DateTimeField()

    class Meta:
        database = database
    '''
    
def create_tables():
    database.connect() # <-- note the explicit call to connect()
    #Member.create_table()
    BlogEntry.create_table()
