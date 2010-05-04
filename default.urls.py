# -*- mode: python; coding: utf-8; -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.sitemaps import FlatPageSitemap
from django.views.decorators.cache import cache_page
from blog.posts.sitemaps import BlogSitemap
from vz_stream.views import view_stream

from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'blog': BlogSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^posts/', include('posts.urls')),
	(r'^users/', include('users.urls')),

    (r'^stream/json/$', cache_page(view_stream, 60*15), {'mimetype': 'application/json'}),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html' }, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	
	(r'^status/cache/$', 'utils.cache_satus.view'),
)
