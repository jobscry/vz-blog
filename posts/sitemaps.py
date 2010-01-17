# -*- mode: python; coding: utf-8; -*-
from django.contrib.sitemaps import Sitemap
from models import Post

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6
    
    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_on

    def location(self, obj):
        return obj.get_absolute_url()
