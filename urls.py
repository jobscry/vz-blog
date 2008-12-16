from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^comments/', include('django.contrib.comments.urls')),

    (r'^posts/', include('blog.posts.urls')),
	(r'^users/', include('blog.users.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),    
	(r'^admin/(.*)', admin.site.root),

	url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'login.html' },name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
