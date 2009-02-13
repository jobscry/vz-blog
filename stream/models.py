from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime, time
from utils import feedparser
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str

user_agent = 'vz-blog/%s +%s'%(settings.BLOG_CODE_VERSION, settings.BLOG_CODE_URL)

class RssFeed(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    times_updated = models.IntegerField(default=0)
    etag = models.CharField(max_length=255, default='', blank=True)
    modified = models.DateTimeField(blank=True, null=True)
    last_status = models.CharField(max_length=25, default='N/A')
    last_debug = models.TextField(default='none')
    escape_html = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def entries(self):
        return Entry.objects.filter(feed=self)

    def __unicode__(self):
        return '%s: %s'%(self.title, self.url)

    def update_entries(self, stream):
        if self.etag != '':
            data = feedparser.parse(self.url, etag=self.etag, agent=user_agent)
        elif self.modified != None:
            d = self.modified
            t_tuple = (d.year, d.month, d.day, d.hour, d.minute, d.second, d.weekday(),  d.toordinal() - datetime.date(d.year, 1, 1).toordinal() + 1, 0)
            data = feedparser.parse(self.url, modified=t_tuple, agent=user_agent)
        else:
            data = feedparser.parse(self.url, agent=user_agent)

        if data.bozo == 1:
             self.debug_message = 'bozo detected'
             self.save()
             return

        if data.has_key('debug_message'):
            self.last_debug = data.debug_message
            self.save()

        self.last_status = data.status
        self.times_updated = self.times_updated+1
        
        if data.has_key('etag') and data.etag:
            self.etag = data.etag
        elif data.has_key('modified') and data.modified:
            self.modified = datetime.datetime(*data.modified[0:6])

        self.save()

        try:
            last_entry = self.entries().all()[0]
        except IndexError:
            last_entry = False
        for entry in data.entries:
            published_on = datetime.datetime(*entry.updated_parsed[0:6])
            if last_entry is False or published_on > last_entry.published_on:
                try:
                    if entry.has_key('summary'):
                        body = smart_str(entry.summary)
                    else:
                        body = smart_str(entry.content)
                    Entry.objects.create(
                        stream=stream,
                        feed=self,
                        title=smart_str(entry.title),
                        link=smart_str(entry.link),
                        body=body,
                        published_on=published_on
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
