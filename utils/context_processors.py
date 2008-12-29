from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from blog.posts.models import Post

def preview_length(request):
    return { 'preview_length': settings.POST_PREVIEW_LENGTH }

def base_url(request):
    current_site = Site.objects.get(id=settings.SITE_ID)
    return { 'base_url': 'http://%s'%current_site.domain }

def flatpage_list(request):
    return { 'flatpages': FlatPage.objects.all().order_by('title') }
