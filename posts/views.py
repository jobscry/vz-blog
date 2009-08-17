from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_index, archive_year, archive_month
from tagging.models import Tag, TaggedItem
from tagging.utils import LINEAR
from utils import render_to_response
from models import Post, Comment
from forms import SearchForm, CommentForm

def moderate_comment(request, action, comment_id):
    """
    Moderate Comment
    
    Logged in users who have permissions to ``comment.can_change``  can either 
    mark comment as ``spam`` or ``approved``
    
    Redirects to comment's post.
    
    Templates:  none
    Context:
        none
    """
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
        posts = TaggedItem.objects.get_by_model(Post, tag).filter(is_published=True)
    else:
        posts = None

    return render_to_response(
        'posts/posts-by-tag.html',
        {
            'tag': tag,
            'post_tags': Tag.objects.cloud_for_model(Post, steps=10, min_count=1, distribution=LINEAR),
            'posts_list': posts,
        },
        request
    )

def archive(request, year, month):
    """
    Archive View
    
    mostly a hackjob from Django's generic date_based views, required because
    jinja2 doesn't play nice with the generic views.
    
    Templates: 
        ``posts/archive-index.html``, 
        ``posts/archive-month.html``,
        ``posts/archive-year.html``
    Context:
        date_list
            list of dates in current archive view
        year
            year for archive view (if provided)
        month
            month for archive view (if provided)
        post_list
            queryset of posts from date
    """
    import datetime, time
    queryset = Post.objects.filter(is_published=True)

    if year is None:    
        return render_to_response(
            'posts/archive-index.html',
            { 'date_list': queryset.dates('published_on', 'year')[::-1] },
            request
        )
    if month is None:
        return render_to_response(
            'posts/archive-year.html',
            {
                'date_list': queryset.filter(published_on__year=year).dates('published_on', 'month'),
                'year': year,
            },
            request
        )

    try:
        date = datetime.date(*time.strptime(year+month, '%Y'+'%m')[:3])
    except ValueError:
        raise Http404

    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {
        'published_on__gte': first_day,
        'published_on__lt': last_day,
    }
    return render_to_response(
        'posts/archive-month.html',
        {
            'posts_list': queryset.filter(**lookup_kwargs),
            'month': date
        },
        request
    )

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
            string to search Post objects for, can be submitted view form or AJAX
        posts
            queryset of posts matching search_string
    """
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
        'posts/search-posts.html',
        {
            'form': form,
            'search_string': search_string,
            'posts': posts,
        },
        request
    )

def posts_list(request, page_num):
    """
    Posts List
    
    Main index view for Post objects.  Returns paginated list of published Posts.
    
    Templates: ``posts/posts-list.html``
    Context:
        post_list
            list of published Posts
        page_obj
            Paginated page object
        paginator
            paginator object
    """
    paginator = Paginator(get_list_or_404(Post, is_published=True), settings.POSTS_PER_PAGE)

    page = paginator.page(page_num)

    return render_to_response(
        'posts/posts-list.html',
        {
            'post_list':  page.object_list,
            'page_obj': page,
            'paginator': paginator
        },
        request
    )

def view_post(request, slug):
    """
    View Post
    
    Views single post, by slug.
    
    If post is not published, only a logged in view with post.can_change permissions
    can view the draft.
    
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
            'related_posts': TaggedItem.objects.get_union_by_model(Post, post.tags).filter(is_published=True).exclude(pk=post.pk),
        },
        request
    )

def comment(request, slug):
    """
    Comment
    
    Creates a comment to a post by slug.
    
    Checks to see if post has comments enabled.
    
    If user is logged in, popluates fields from profile.
    
    After comment is created, send email to posts' author notifying of new comment
    in moderation queue.
    
    Templates: ``posts/comment-form.html``
    Context:
        post
            post object to comment on
        form
            CommentForm object
    """
    post = get_object_or_404(Post, slug=slug)

    if not post.can_comment:
        return HttpResponseForbidden('This post is closed for comments.')

    if request.method == 'POST':
        form = CommentForm(post, data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if settings.DEBUG:
                comment.author_ip = '127.0.0.1'
            else:
                comment.author_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
            comment.author_user_agent = request.META.get('HTTP_USER_AGENT', '')
            comment.author_refferrer = request.META.get('HTTP_REFERER', '')
            comment.save()
            
            from django.core.mail import send_mail

            current_site = Site.objects.get(id=settings.SITE_ID)
            post.comments.add(comment)
            if settings.BLOG_NOTIFY_ON_COMMENT:
                if request.user.is_authenticated():
                    comment.user = request.user
                    comment.mark_approved()
                    send_mail(
                        u'[%s :: registered user comment]'%settings.BLOG_TITLE,
                        u'A comment has been made by %s <%s> on %s.\n\r  See it at http://%s%s#c%s'%(
                            request.user.username,
                            request.user.email,
                            post.title,
                            current_site.domain,
                            post.get_absolute_url(),
                            comment.pk
                        ),
                        settings.EMAIL_HOST_USER,
                        (post.author.email, ),
                        fail_silently=True
                    )
                else:
                    send_mail(
                        u'[%s :: comment awaiting moderation]'%settings.BLOG_TITLE,
                        u'A comment has been made by %s <%s> from %s on %s.\n\r  Moderate it at http://%s%s#c%s'%(
                            comment.author_name,
                            comment.author_email,
                            comment.author_ip,
                            post.title,
                            current_site.domain,
                            post.get_absolute_url(),
                            comment.pk
                        ),
                        settings.EMAIL_HOST_USER,
                        (post.author.email, ),
                        fail_silently=True
                    )
                
            return render_to_response(
                'posts/comment-submitted.html',
                {
                    'post': post,
                    'comment':  comment
                },
                request
            )

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

    return render_to_response(
        'posts/comment-form.html',
        {
            'post': post,
            'form': form
        },
        request
    )
