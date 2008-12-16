from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from tagging.fields import TagField
from datetime import datetime

class Comment(models.Model):
    author_name = models.CharField(max_length="255")
    author_email = models.EmailField()
    author_url = models.URLField()
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)  
    added_on = models.DateTimeField(auto_now_add=True)  

    def __unicode__(self):
        return u'%s by %s on %s'%(self.pk, self.author_name, self.added_on.strftime('%c'))

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
    update_pingbacks = models.BooleanField(default=False)
    comments_enabled = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    published_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True, null=True, through='CommentsToPosts')

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('posts.views.view_post', [self.slug])

    class Meta:
        ordering = ['-published_on', 'title']

class CommentsToPosts(models.Model):
    comment = models.ForeignKey(Comment)
    post = models.ForeignKey(Post)
    
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
        import pingback
        
        current_site = Site.objects.get(id=settings.SITE_ID)
        html = markdown.markdown(force_unicode(instance.body))
        pingback.autoPingback('http://%s'%current_site.domain, reST=None, HTML=html)

post_save.connect(auto_pingback, sender=Post)

#http://sciyoshi.com/blog/2008/aug/27/using-akismet-djangos-new-comments-framework/
from django.contrib.comments.signals import comment_was_posted

def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    try:
        from akismet import Akismet
    except:
        return

    ak = Akismet(
        key=settings.AKISMET_API_KEY,
        blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )

    if ak.verify_key():
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'comment_type': 'comment',
            'comment_author': comment.user_name.encode('utf-8'),
        }

        if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
            comment.flags.create(
                user=comment.content_object.author,
                flag='spam'
            )
            comment.is_public = False
            comment.save()

comment_was_posted.connect(on_comment_was_posted)
