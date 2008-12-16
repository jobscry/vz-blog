from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_detail
from django.views.generic.date_based import archive_index, archive_year, archive_month
from django.template import RequestContext
from tagging.models import Tag, TaggedItem
from models import Post
from forms import SearchForm


def posts_by_tag(request):
    tag = request.GET.get('tag', None)
    posts = TaggedItem.objects.get_by_model(Post, tag).filter(is_published=True)

    return render_to_response(
        'posts-by-tag.html',
        {
            'tag': tag,
            'posts': posts,
        },
        context_instance=RequestContext(request)
    )

def archive(request, year, month):
    queryset = Post.objects.filter(is_published=True)
    date_field = 'published_on'    

    if year is None:    
        return archive_index(
            request,
            queryset,
            date_field,
            template_name='archive-index.html',
            template_object_name='posts',        
        )
    if month is None:
        return archive_year(
            request,
            year,
            queryset,
            date_field,
            template_name='archive-year.html',
            template_object_name='posts',        
        )
    return archive_month(
        request,
        year,
        month,
        queryset,
        date_field,
        month_format='%m',
        template_name='archive-month.html',
        template_object_name='posts',        
    )    

def search_posts(request):
    search_string = request.GET.get('search_string', None)
    if search_string != None:
        form =     SearchForm(request.GET)
        posts = Post.objects.filter(
            Q(is_published=True),            
            Q(title__contains=search_string) | Q(body__contains=search_string)
        )
    else:
        form =     SearchForm()
        posts = None
    return render_to_response(
        'search-posts.html',
        {
            'form': form,
            'search_string': search_string,
            'posts': posts,
        },
        context_instance=RequestContext(request)
    )

def posts_list(request):
    return render_to_response(
        'posts-list.html',
        {
            'posts': Post.objects.filter(is_published=True),
        },
        context_instance=RequestContext(request)
    )

def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.is_published == False:
        if request.user.has_perms('posts.post.can_change') == False:
            return HttpResponseNotAllowed('You cannot view this post.')

    related_posts = TaggedItem.objects.get_union_by_model(Post, post.tags).filter(is_published=True).exclude(pk=post.pk)

    return render_to_response(
        'view-post.html',
        {
            'post': post,
            'related_posts': related_posts,
        },
        context_instance=RequestContext(request)
    )
