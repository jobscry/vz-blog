# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.conf.urls.defaults import *
from posts.feeds import LatestPosts
from posts.models import Post

from django.views.generic import date_based

archive = {
    'queryset': Post.objects.filter(is_published=True).only('title', 'slug', 'published_on'),
    'date_field': 'published_on',
    'allow_empty': True,
    'template_object_name': 'post'
}

urlpatterns = patterns('',
    url(r'archive/$', date_based.archive_index, archive, name='archive_index'),
    url(r'archive/(?P<year>\d{4})/$', date_based.archive_year, archive, name='archive_year'),
    url(r'archive/(?P<year>\d{4})/(?P<month>\d{1,2})', date_based.archive_month,
        dict({'month_format': '%m'}, **archive), name='archive_month')
)

feeds = {
    'latest': LatestPosts,
    #'tags': PostsByTag,
}

urlpatterns += patterns('',
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('posts.views',
	url(r'search/$', 'search_posts', name="search_posts"),
	url(r'tags/$', 'posts_by_tag', name="posts_by_tag"),
	url(r'(?P<slug>[\w\-]+)/$', 'view_post', name="view_post"),
)

from django.views.generic import list_detail

urlpatterns += patterns('',
    url(r'', list_detail.object_list, 
        {'queryset': Post.objects.filter(is_published=True).only(
            'title', 'slug', 'author', 'published_on', 'body', 'tags'), 
            'paginate_by': settings.POSTS_PER_PAGE,
            'template_object_name': 'post', 'extra_context': {'do_truncate': True}},
            name='post_list'
    )
)
