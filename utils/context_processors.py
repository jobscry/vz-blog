from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from tagging.models import Tag
from tagging.utils import LOGARITHMIC
from blog.posts.models import Post
from blog.links.models import Link

def blog_info(request):
    return { 
        'blog_tagline': settings.BLOG_TAGLINE,
        'blog_title': settings.BLOG_TITLE,
        'blog_copyright': settings.BLOG_COPYRIGHT,
        'blog_copyright_url': settings.BLOG_COPYRIGHT_URL,
        'blog_preview_length': settings.POST_PREVIEW_LENGTH,
        'blog_linkroll': Link.objects.all(),
        'blog_tags': Tag.objects.cloud_for_model(Post, steps=10, min_count=1, distribution=LOGARITHMIC),
    }

def base_url(request):
    current_site = Site.objects.get(id=settings.SITE_ID)
    return { 'base_url': 'http://%s'%current_site.domain }

def extra_meta(request):
    return { 'extra_meta': settings.EXTRA_META }

def flatpage_list(request):
    return { 'flatpages': FlatPage.objects.all().order_by('title') }
