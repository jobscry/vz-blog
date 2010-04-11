# -*- mode: python; coding: utf-8; -*-
from itertools import chain
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.context import get_standard_processors

from jinja2 import PackageLoader, Environment, ChoiceLoader, FileSystemLoader, TemplateNotFound, MemcachedBytecodeCache

from os import path

_jinja_env = None

default_mimetype = settings.DEFAULT_CONTENT_TYPE

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
    
    bytecode_cache=None
    try:
        import re, cmemcache
        m = re.match(
        "memcached://([.\w]+:\d+)", settings.CACHE_BACKEND
        )
        if m:
            mc = cmemcache.Client([m.group(1)], debug=0)
            bytecode_cache = MemcachedBytecodeCache(mc)
    except ImportError:
        pass

    env = Environment(loader=ChoiceLoader(loader_array), autoescape=True, bytecode_cache=bytecode_cache, extensions=[Compressor])

    from django.template.defaultfilters import date
    env.filters['date'] = date
    
    from django.template.defaultfilters import truncatewords_html, pluralize, removetags
    env.filters['truncatewords_html'] = truncatewords_html
    env.filters['makeplural'] = pluralize
    env.filters['removetags'] = removetags

    from django.contrib.humanize.templatetags.humanize import naturalday, apnumber
    env.filters['naturalday'] = naturalday
    env.filters['apnumber'] = apnumber

    from posts.templatetags.post_extras import markdowner, esvapi
    env.filters['markdown'] = markdowner
    env.filters['esv'] = esvapi

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
    context['request'] = request
    for processor in chain(get_standard_processors(), processors or ()):
        context.update(processor(request))
    return get_template(template_name).render(context)

def render_to_response(template_name, context=None, request=None,
                       processors=None, mimetype=default_mimetype):
    """Render a template into a response object."""
    return HttpResponse(render_to_string(template_name, context, request,
                                         processors), mimetype)

from jinja2 import nodes
from jinja2.ext import Extension
from django.core.cache import cache
from compressor import CssCompressor, JsCompressor
from compressor.conf import settings as c_settings

class Compressor(Extension):
    tags = set(['compress'])
    
    def __init__(self, environment):
        super(Compressor, self).__init__(environment)

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompress'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_compress', args),
                               [], [], body).set_lineno(lineno)

    def _compress(self, kind, caller):
        content = caller()
        if not c_settings.COMPRESS:
            return content
        if kind == 'css':
            compressor = CssCompressor(content)
        if kind == 'js':
            compressor = JsCompressor(content)
        in_cache = cache.get(compressor.cachekey)
        if in_cache:
            return in_cache
        else:
            # do this to prevent dog piling
            in_progress_key = 'django_compressor.in_progress.%s' % compressor.cachekey
            in_progress = cache.get(in_progress_key)
            if in_progress:
                while cache.get(in_progress_key):
                    sleep(0.1)
                output = cache.get(compressor.cachekey)
            else:
                cache.set(in_progress_key, True, 300)
                try:
                    output = compressor.output()
                    cache.set(compressor.cachekey, output, 2591000) # rebuilds the cache every 30 days if nothign has changed.
                except:
                    from traceback import format_exc
                    raise Exception(format_exc())
                cache.set(in_progress_key, False, 300)
            return output

    def _get_compressor_output(self, compressor):
        if not c_settings.COMPRESS:
            return compressor.content
        url = "%s/%s" % (settings.MEDIA_URL.rstrip('/'), compressor.new_filepath)
        compressor.save_file()
        context = getattr(compressor, 'extra_context', {})
        context['url'] = url
        return render_to_string(compressor.template_name, context)
