from django.conf.urls.defaults import *

urlpatterns = patterns('stream.views',
    url(r'ajax/$', 'view_stream', { 'pk': 1, }),
    url(r'$', 'view_stream', { 'pk': 1, }, name="view_stream"),
)
