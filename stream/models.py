from django.db import models
from django.contrib.auth.models import User
import datetime, time
from utils import feedparser
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
      

class RssFeed(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    times_updated = models.IntegerField(default=0)
    etag = models.CharField(max_length=255, default='', blank=True)
    modified = models.DateTimeField(blank=True, null=True)
    last_status = models.CharField(max_length=25, default='N/A')
    escape_html = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def entries(self):
        return Entry.objects.filter(feed=self)

    def __unicode__(self):
        return '%s: %s'%(self.title, self.url)

    def update_entries(self, stream):
        if self.etag == '' and self.modified == None:
            data = feedparser.parse(self.url)
        elif self.etag != '':
            data = feedparser.parse(self.url, etag=self.etag)
        else:
            d = self.modified
            t_tuple = time.mktime( (d.year, d.month, d.day, d.hour, d.minute, d.second, d.weekday(),  d.toordinal() - datetime.date(d.year, 1, 1).toordinal() + 1, 0) )
            data = feedparser.parse(self.url, modified=t_tuple)

        if 'status' not in data.keys() or data.status != 200:
            return

        self.last_status = data.status
        self.times_updated = self.times_updated+1
        
        if data.etag:
            loc = data.etag.find('-')
            if loc > -1:
                self.etag = data.etag[:loc]
            else:
                self.etag = data.etag
        elif data.modified:
            self.modified = datetime.datetime(*data.modified[0:6])

        self.save()

        for entry in data.entries:
            try:
                Entry.objects.create(
                    stream=stream,
                    feed=self,
                    title=smart_str(entry.title),
                    link=smart_str(entry.link),
                    body=smart_str(entry.summary),
                    published_on=datetime.datetime(
                        entry.updated_parsed[0],
                        entry.updated_parsed[1],
                        entry.updated_parsed[2],
                        entry.updated_parsed[3],
                        entry.updated_parsed[4],
                        entry.updated_parsed[5]
                    )
                )
            except DjangoUnicodeDecodeError:
                pass

class Stream(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, default='default')
    rss_feeds = models.ManyToManyField(RssFeed, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s: %s'%(self.user.username, self.name)

    def update_feeds(self):
        for feed in self.rss_feeds.all():
            feed.update_entries(self)

class Entry(models.Model):
    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-published_on']
    stream = models.ForeignKey(Stream)
    feed = models.ForeignKey(RssFeed)
    link = models.URLField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    published_on = models.DateTimeField(blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s: %s'%(self.stream, self.title)
