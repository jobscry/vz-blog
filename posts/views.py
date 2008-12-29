from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_index, archive_year, archive_month
from tagging.models import Tag, TaggedItem
from models import Post, Comment
from forms import SearchForm, CommentForm

def moderate_comment(request, action, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = get_object_or_404(Post, comments=comment)
    
    if post.is_published == False:
        return HttpResponseNotAllowed('You cannot comment on this post.')
    
    if action == 'approved':
        comment.mark_approved()
    elif action == 'spam':
        comment.mark_spam()
    else:
        return HttpResponseNotAllowed('Action must be either "spam" or "approved".')

    return HttpResponseRedirect(post.get_absolute_url())
moderate_comment = permission_required('comment.can_change')(moderate_comment)

def posts_by_tag(request):
    tag = request.GET.get('tag', None)
    if tag != None:
        posts = TaggedItem.objects.get_by_model(Post, tag).filter(is_published=True)
    else:
        posts = None

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
    from django.db.models import Q
    search_string = request.GET.get('search_string', None)
    if search_string != None:
        form =     SearchForm(request.GET)
        posts = Post.objects.filter(
            Q(is_published=True),            
            Q(title__contains=search_string) | Q(body__contains=search_string)
        )
    else:
        form =  SearchForm()
        posts = None

    if request.is_ajax():
        from django.core import serializers
        if posts != None:
            data = serializers.serialize(
                'json',
                posts, 
                fields=('title', 'slug', 'published_on')
        )
        else:
            data = None
        response = HttpResponse(mimetype='application/json')
        response.write(data)
        return response

    return render_to_response(
        'search-posts.html',
        {
            'form': form,
            'search_string': search_string,
            'posts': posts,
        },
        context_instance=RequestContext(request)
    )

def posts_list(request, page):
    return object_list(
        request,
        Post.objects.filter(is_published=True),
        paginate_by=settings.POSTS_PER_PAGE,
        page=page,
        template_name='posts-list.html',
        template_object_name='post',
    )

def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.is_published == False:
        if request.user.has_perms('posts.post.can_change') == False:
            return HttpResponseNotAllowed('You cannot view this post.')

    related_posts = TaggedItem.objects.get_union_by_model(Post, post.tags).filter(is_published=True).exclude(pk=post.pk)
    
    if post.can_comment:
        if request.method == 'POST':
            form = CommentForm(post, request.POST)
            if form.is_valid():
                comment = form.save()
                if request.user.is_authenticated():
                    comment.mark_approved()
                post.comments.add(comment)

        if request.user.is_authenticated():
            current_site = Site.objects.get(id=settings.SITE_ID)
            form = CommentForm(
                post,
                initial = {
                    'author_name': request.user.username,
                    'author_email': request.user.email,
                    'author_url': u'http://%s'%current_site.domain,
                }
            )
        else:
            form = CommentForm(post)
    else:
        form = None
        

    return render_to_response(
        'view-post.html',
        {
            'post': post,
            'related_posts': related_posts,
            'form': form,
        },
        context_instance=RequestContext(request)
    )
