# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from tagging.fields import TagField

class Post(models.Model):
    """
    Post

    Post model for blog
    """
    author = models.ForeignKey(User)
    title = models.CharField(max_length="255")
    slug = models.SlugField(unique=True)
    tags = TagField()
    body = models.TextField()
    update_pingbacks = models.BooleanField(default=False, help_text="Automagically discover and update pingbacks?")
    is_published = models.BooleanField("Published", default=False, help_text="Publish this post?")
    published_on = models.DateTimeField("Date Published", blank=True, null=True, help_text="Manually change the date this post was published on.")
    created_on = models.DateTimeField("Date Created", auto_now_add=True)

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('posts.views.view_post', [self.slug])

    class Meta:
        ordering = ['-published_on', 'title']


def auto_set_published_on(sender, instance, created, **kwargs):
    """
    Auto Set Published On
    """
    if instance.is_published and instance.published_on == None:
        instance.published_on = datetime.today()
        instance.save()

post_save.connect(auto_set_published_on, sender=Post)

def auto_pingback(sender, instance, created, **kwargs):
    """
    Auto Pingback
    
    using http://mathieu.fenniak.net/python-pingback-library/
    Automagically handles pingback when post is published
    """
    if instance.update_pingbacks:
        from django.utils.encoding import force_unicode
        import markdown
        import utils.pingback
        
        current_site = Site.objects.get(id=settings.SITE_ID)
        html = markdown.markdown(force_unicode(instance.body))
        try:
            pingback.autoPingback('http://%s'%current_site.domain, reST=None, HTML=html)
        except:
            pass

post_save.connect(auto_pingback, sender=Post)
