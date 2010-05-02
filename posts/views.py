# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_list_or_404, get_object_or_404, \
    render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_index, archive_year, \
    archive_month
from tagging.models import Tag, TaggedItem
from tagging.utils import LINEAR
from posts.models import Post
from posts.forms import SearchForm


def posts_by_tag(request):
    """
    Posts by Tag

    Gets all posts that are taged tag from GET request if it exists.

    Templates:  ``posts/posts-by-tag.html``
    Context:
        tag
            string tag from GET request
        post_tags
            Tag cloud from Tag.objects.cloud_for_model
        posts_list
            all posts with tag
    """
    tag = request.GET.get('tag', None)
    if tag != None:
        posts = TaggedItem.objects.get_by_model(Post, tag).filter(
        `is_published=True).only('title', 'slug', 'published_on')
    else:
        posts = None

    return render_to_response(
        'posts/posts-by-tag.html',
        {
            'tag': tag,
            'post_tags': Tag.objects.cloud_for_model(
                Post, steps=10, min_count=1, distribution=LINEAR),
            'post_list': posts,
        },
        context_instance=RequestContext(request))


def search_posts(request):
    """
    Search Posts

    Uses django Q object to search Post objects within title and body fields.

    Can also be called via AJAX.  If so, returns JSON serialized Post objects.

    Templates: ``posts/search-posts.html``
    Context:
        form
            SearchForm object
        search_string
            string to search Post objects for, can be submitted view form or
            AJAX
        posts
            queryset of posts matching search_string
    """
    from django.db.models import Q
    search_string = request.GET.get('search_string', None)
    if search_string != None:
        form = SearchForm(request.GET)
        post_list = Post.objects.filter(
            Q(is_published=True),
            Q(title__contains=search_string) | \
            Q(body__contains=search_string)).only('
            title', 'slug', 'published_on')
    else:
        form = SearchForm()
        post_list = None

    if request.is_ajax():
        from django.core import serializers
        if post_list != None:
            data = serializers.serialize(
                'json', post_list, fields=('title', 'slug', 'published_on'))
        else:
            data = None
        response = HttpResponse(mimetype='application/json')
        response.write(data)
        return response

    return render_to_response(
        'posts/search-posts.html',
        {
            'form': form,
            'search_string': search_string,
            'post_list': post_list,
        },
        context_instance=RequestContext(request))


def view_post(request, slug):
    """
    View Post

    Views single post, by slug.

    If post is not published, only a logged in view with post.can_change
    permissions can view the draft.

    Templates: ``posts/view-post.html``
    Context:
        post
            post object
        related_posts
            queryset of posts with matching tags from TaggedItem.objects.
            get_union_by_model
    """
    post = get_object_or_404(Post, slug=slug)
    if post.is_published == False:
        if request.user.has_perms('posts.post.can_change') == False:
            return HttpResponseNotAllowed('You cannot view this post.')

    return render_to_response(
        'posts/view-post.html',
        {
            'post': post,
            'related_posts': TaggedItem.objects.get_union_by_model(
                Post, post.tags).filter(is_published=True).only(
                    'title', 'slug', 'published_on').exclude(pk=post.pk),
        },
        context_instance=RequestContext(request))
