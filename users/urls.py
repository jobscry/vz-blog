from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
    url(r'edit/profile/(?P<username>[\w\-]+)/$', 'edit_profile', name="edit_profile"),
    url(r'profile/$', 'view_profile', { 'username': None }, name="my_profile"),
    url(r'profile/(?P<username>[\w\-]+)/$', 'view_profile', name="view_profile"),
)
