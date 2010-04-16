# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from models import Post

class LatestPosts(Feed):
    
    def title(self):
        return settings.BLOG_TITLE

    def link(self):
        current_site = Site.objects.get(id=settings.SITE_ID)
        return 'http://%s/posts/feed/latest/'%current_site.domain

    def description(self):
        return settings.BLOG_TAGLINE

    def author_name(self):
        return settings.ADMINS[0][0]

    def author_email(self):
        return settings.ADMINS[0][1]

    def author_link(self):
        current_site = Site.objects.get(id=settings.SITE_ID)
        return 'http://%s/'%current_site.domain

    def copyright(self):
        return settings.BLOG_COPYRIGHT

    def items(self):
        return Post.objects.filter(is_published=True).order_by('-published_on')[:10]

    def item_description(self, item):
        return item.body

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_author_email(self, item):
        return item.author.email

    def item_pubdate(self, item):
        return item.published_on

    def item_categories(self, item):
        return item.tags.split(' ')

    def item_copyright(self):
        return settings.BLOG_COPYRIGHT
