from feedformatter import Feed

FEED_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
FEED_TEMPLATE = "%s \n %s"


class FeedGenerator(object):
    def __init__(self, **kwargs):
        self.feed = Feed()
        self.header = FEED_HEADER

        for k, v in kwargs.items():
            self.add_meta(k, v)

    def add_meta(self, label, val):
        self.feed.feed[label] = val

    def add_item(self, title, link, desc='', pub_date='', post_id=''):
        self.feed.items.append({
            'title': title,
            'link': link,
            'description': desc,
            'pubDate': pub_date.utctimetuple() if pub_date else None,
            'guid': post_id,
        })

    def render(self, format='rss'):
        if format.lower().count('atom'):
            feed_str = self.feed.format_atom_string()
        else:
            feed_str = self.feed.format_rss2_string()

        return FEED_TEMPLATE % (self.header, feed_str)

    def rss(self):
        return self.render('rss')

    def atom(self):
        return self.render('atom')
