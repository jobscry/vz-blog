# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import smart_unicode
from utils.akismet import Akismet
from utils.jinja2_utils import render_to_string
from tagging.fields import TagField
from datetime import datetime, timedelta

class Comment(models.Model):
    author_name = models.CharField('Name', max_length="255")
    author_email = models.EmailField('Email')
    author_url = models.URLField('URL', verify_exists=False, null=True, blank=True)
    author_ip = models.IPAddressField('IP Address')
    author_user_agent = models.CharField('User Agent', max_length="255")
    author_referrer = models.CharField('Referrer', max_length="255", null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, default='')
    body = models.TextField()
    is_approved = models.BooleanField(default=False, help_text="Approve this comment?")
    is_spam = models.BooleanField(default=False, help_text="Is this comment SPAM?")  
    awaiting_moderation = models.BooleanField(default=True, help_text="Is this comment in the moderation queue?")
    added_on = models.DateTimeField(auto_now_add=True)  

    def __unicode__(self):
        return u'%s by %s on %s'%(self.pk, self.author_name, self.added_on.strftime('%c'))

    def mark_approved(self):
        """
        Mark Approved
        
        If comment was mistakenly marked as SPAM by Akismet, mark approved, then send HAM.
        """
        if self.is_spam:
            ak = _get_ak()
            if ak.verify_key():
                data = _build_comment_data(self)
                ak.suubmit_ham(smart_unicode(instance.body), data=data, build_data=True)

        self.is_approved = True
        self.awaiting_moderation = False
        self.is_spam = False
        self.save()
    
    def mark_spam(self):
        """
        Mark SPAM
        
        If Akismet didn't catch it, mark as SPAM and submit it to Akismet
        """
        if self.is_spam == False:        
            ak = _get_ak()
            if ak.verify_key():
                data = _build_comment_data(self)
                ak.submit_spam(smart_unicode(self.body), data=data, build_data=True)

        self.is_approved = False
        self.awaiting_moderation = False
        self.is_spam = True
        self.save()

    class Meta:
        permissions = (
            ("can_moderate", 'Can moderate'),
            ("can_add", 'Can add'),
            ("can_remove", 'Can remove'),
        )
        ordering = ['added_on',]   

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
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    comments_enabled = models.BooleanField(default=True)
    override_max_comment_age = models.BooleanField(default=False, help_text="Allow comments even after MAX_COMMENT_DAYS?")
    is_published = models.BooleanField("Published", default=False, help_text="Publish this post?")
    published_on = models.DateTimeField("Date Published", blank=True, null=True, help_text="Manually change the date this post was published on.")
    created_on = models.DateTimeField("Date Created", auto_now_add=True)

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('posts.views.view_post', [self.slug])

    def approved_comments(self):
        return self.comments.filter(is_approved=True)
    
    def moderation_queue(self):
        return self.comments.filter(awaiting_moderation=True)

    def can_comment(self):
        if self.is_published and self.comments_enabled:
            if self.override_max_comment_age:
                return True
            delta_date = timedelta(days=settings.MAX_COMMENT_DAYS)
            now = datetime.now()
            max_date = self.published_on + delta_date
            if now < max_date:
                return True
        return False

    class Meta:
        ordering = ['-published_on', 'title']

    def can_comment(self):
        if self.is_published and self.comments_enabled:
            if self.override_max_comment_age:
                return True
            delta_date = timedelta(days=settings.MAX_COMMENT_DAYS)
            now = datetime.now()
            max_date = self.published_on + delta_date
            if now < max_date:
                return True
        return False

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

#http://sciyoshi.com/blog/2008/aug/27/using-akismet-djangos-new-comments-framework/

def comment_akismet_check(sender, instance, **kwargs):
    """
    Comment Akismet Check
    
    Check all incoming comments against Akismet
    """
    if instance.is_spam == False:
        ak = _get_ak()
        if ak.verify_key():
            data = _build_comment_data(instance)
            if ak.comment_check(smart_unicode(instance.body), data=data, build_data=True):
                instance.is_spam = True

post_save.connect(comment_akismet_check, sender=Comment)

def _get_ak():
    return Akismet(
        key=settings.AKISMET_API_KEY,
        blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )

def _build_comment_data(comment):
    return {
        'user_ip': smart_unicode(comment.author_ip),
        'user_agent': smart_unicode(settings.BLOG_USER_AGENT),
        'referrer': smart_unicode(comment.author_referrer),
        'comment_type': 'comment',
        'comment_author': smart_unicode(comment.author_name),
    }
