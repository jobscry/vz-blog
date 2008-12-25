from django.conf import settings
from django.contrib.sites.models import Site
from blog.posts.models import Post

def base_url(request):
    current_site = Site.objects.get(id=settings.SITE_ID)
    return { 'base_url': 'http://%s'%current_site.domain }
    
