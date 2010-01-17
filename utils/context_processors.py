# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.cache import cache
from tagging.models import Tag
from tagging.utils import LOGARITHMIC
from blog.posts.models import Post
from blog.links.models import Link

import blog

def blog_info(request):
    linkroll = cache.get('blog_linkroll', None)
    if linkroll is None:
        cache.set('blog_linkroll',  Link.objects.all(), 60*15)
        linkroll = cache.get('blog_linkroll')

    tags = cache.get('blog_tags', None)
    if tags is None:
        cache.set('blog_tags',  Tag.objects.cloud_for_model(Post, steps=10, min_count=1, distribution=LOGARITHMIC), 60*15)
        tags = cache.get('blog_tags')
    return { 
        'blog_tagline': settings.BLOG_TAGLINE,
        'blog_title': settings.BLOG_TITLE,
        'blog_copyright': settings.BLOG_COPYRIGHT,
        'blog_copyright_url': settings.BLOG_COPYRIGHT_URL,
        'blog_version': blog.__version__,
        'blog_preview_length': settings.POST_PREVIEW_LENGTH,
        'blog_linkroll': linkroll,
        'blog_tags': tags,
        'blog_feedburner_url': settings.FEEDBURNER_URL,
    }

def base_url(request):
    site = cache.get('current_site', None)
    if site is None:
        cache.set('current_site', Site.objects.get(id=settings.SITE_ID).domain, 60*15)
        site = cache.get('current_site')
    return { 'base_url': 'http://%s'%site }

def extra_meta(request):
    return { 'extra_meta': settings.EXTRA_META }

def google_analytics_js(request):
    return { 'google_analytics_js': settings.GOOGLE_ANALYTICS_JS }

def flatpage_list(request):
    return { 'flatpages':  FlatPage.objects.all().order_by('title') }

def disqus(request):
    if settings.DISQUS:
        return {
            'disqus': True,
            'disqus_iframe': settings.DISQUS_IFRAME,
            'disqus_js': settings.DISQUS_JS
        }
    else:
        return { 'disqus': False }
