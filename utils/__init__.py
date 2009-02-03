#http://svn.python.org/projects/external/Jinja-1.1/docs/src/devrecipies.txt

from django.http import HttpResponse
from django.template.context import get_standard_processors
from jinja2 import Environment, FileSystemLoader
from django.conf import settings

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

def get_env():
    env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIRS), autoescape=True)

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

def render_to_response(template, context, request=None):
    env = get_env()
    template = env.get_template(template)
    if request:
        for processor in get_standard_processors():
            context.update(processor(request))
    return HttpResponse(template.render(context))
