from django.conf.urls.defaults import *
from django.contrib.sitemaps import FlatPageSitemap
from blog.posts.sitemaps import BlogSitemap

from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'blog': BlogSitemap,
    'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    #(r'^comments/', include('django.contrib.comments.urls')),

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^posts/', include('blog.posts.urls')),
	(r'^users/', include('blog.users.urls')),
	(r'^stream/', include('blog.stream.urls')),	

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),    
	(r'^admin/(.*)', admin.site.root),

    url(r'^login/$', 'users.views.login', name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
) 
