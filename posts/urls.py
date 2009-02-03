from django.conf.urls.defaults import *
from feeds import LatestPosts

feeds = {
    'latest': LatestPosts,
    #'tags': PostsByTag,
}

urlpatterns = patterns('',
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('posts.views',
	url(r'comments/mark/(?P<action>spam|approved)/(?P<comment_id>\d+)/$', 'moderate_comment', name="moderate_comment"),
	url(r'(?P<slug>[\w\-]+)/comment/$', 'comment', name="comment"),
	url(r'archive/$', 'archive', { 'year': None, 'month': None, }, name="archive_index"),
	url(r'archive/(?P<year>\d{4})$', 'archive', { 'month': None, }, name="archive_year"),
	url(r'archive/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'archive', name="archive_month"),
	url(r'search/$', 'search_posts', name="search_posts"),
	url(r'tags/$', 'posts_by_tag', name="posts_by_tag"),
    url(r'page(?P<page>[0-9]+)/$', 'posts_list', name="posts_list_page"),
	url(r'(?P<slug>[\w\-]+)/$', 'view_post', name="view_post"),
    url(r'$', 'posts_list', { 'page_num': 1, }, name="posts_list"),
)

