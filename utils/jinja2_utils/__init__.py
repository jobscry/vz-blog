#http://svn.python.org/projects/external/Jinja-1.1/docs/src/devrecipies.txt

from itertools import chain
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.context import get_standard_processors
from jinja2 import PackageLoader, Environment, ChoiceLoader, FileSystemLoader, TemplateNotFound
from jinja2.defaults import DEFAULT_NAMESPACE
from django.conf import settings

from os import path

from django.core import cache

default_mimetype = settings.DEFAULT_CONTENT_TYPE

_jinja_env = None

def get_env():
    """Get the Jinja2 env and initialize it if necessary."""
    global _jinja_env
    if _jinja_env is None:
        _jinja_env = create_env()
    return _jinja_env

def create_env():
    loader_array = []
    for pth in settings.TEMPLATE_DIRS:
        loader_array.append(FileSystemLoader(pth))

    for app in settings.INSTALLED_APPS:
        loader_array.append(PackageLoader(app))

    env = Environment(loader=ChoiceLoader(loader_array), autoescape=True)

    from django.template.defaultfilters import date
    env.filters['date'] = date

    from django.template.defaultfilters import truncatewords_html, pluralize, removetags
    env.filters['truncatewords_html'] = truncatewords_html
    env.filters['makeplural'] = pluralize
    env.filters['removetags'] = removetags

    from django.contrib.humanize.templatetags.humanize import naturalday, apnumber
    env.filters['naturalday'] = naturalday
    env.filters['apnumber'] = apnumber

    from posts.templatetags.post_extras import markdown
    env.filters['markdown'] = markdown
    
    env.filters['url'] = url
    
    return env

def url(view_name, *args, **kwargs):
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        try:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            return reverse(project_name + '.' + view_name,
                           args=args, kwargs=kwargs)
        except NoReverseMatch:
            return ''

def get_template(template_name, globals=None):
    """Load a template."""
    try:
        return get_env().get_template(template_name, globals=globals)
    except TemplateNotFound, e:
        raise TemplateDoesNotExist(str(e))


def select_template(templates, globals=None):
    """Try to load one of the given templates."""
    env = get_env()
    for template in templates:
        try:
            return env.get_template(template, globals=globals)
        except TemplateNotFound:
            continue
    raise TemplateDoesNotExist(', '.join(templates))

def render_to_string(template_name, context=None, request=None,
                     processors=None):
    """Render a template into a string."""
    context = dict(context or {})
    if request is not None:
        context['request'] = request
        for processor in chain(get_standard_processors(), processors or ()):
            context.update(processor(request))
    return get_template(template_name).render(context)

def render_to_response(template_name, context=None, request=None,
                       processors=None, mimetype=default_mimetype):
    """Render a template into a response object."""
    return HttpResponse(render_to_string(template_name, context, request,
                                         processors), mimetype)
