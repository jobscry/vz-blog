from django.conf import settings
from django.contrib import comments
from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.template import TemplateDoesNotExist
from jinja2 import environmentfilter, Markup
from utils.jinja2_utils import select_template, render_to_string

def comment_count(obj):
    return _qs(obj).count()

def comment_list(obj):
    return _qs(obj)

@environmentfilter
def render_comment_form(env, obj):
    ctype = ContentType.objects.get_for_model(obj)
    form = comments.get_form()(ctype.get_object_for_this_type(pk=obj.pk))

    template_search_list = [
        "comments/%s/%s/form.html" % (ctype.app_label, ctype.model),
        "comments/%s/form.html" % ctype.app_label,
        "comments/form.html"
    ]
    try:
        template = select_template(template_search_list)
    except TemplateDoesNotExist:
        return ''
    rendered = template.render(
        {
            'comment_form':form,
            'comment_form_target': comments.get_form_target()
        }
    )
    if env.autoescape:
        return Markup(rendered)
    else:
        return rendered
    
def _qs(obj):
    ctype = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=ctype, object_pk=obj.pk,
                                  is_public=True)
