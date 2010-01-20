# -*- mode: python; coding: utf-8; -*-
#http://www.martin-geber.com/thought/2007/10/27/markdown-syntax-highlighting-django/
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

import urllib
import re
import markdown

register = template.Library()

try:
    ESV_API_URL = settings.ESV_API_URL
except AttributeError:
    ESV_API_URL = 'http://www.esvapi.org/v2/rest/passageQuery?'

ESV_DICT = {}
ESV_DICT['output-format'] = 'html'
ESV_DICT['include-footnotes'] = 0
ESV_DICT['include-passage-references'] = 1
ESV_DICT['include-first-verse-numbers'] = 0
ESV_DICT['include-passage-horizontal-lines'] = 0
ESV_DICT['include-heading-horizontal-lines'] = 0
ESV_DICT['include-headings'] = 0
ESV_DICT['key'] = 'ip'

BIBLE_RE = re.compile(r'\[\[bible ([^\]]+)\]\]', re.I)

ESV_QUERY_METHOD = 'passage'
ESV_QUERY_URL = ''

@register.filter(name='esv')
@stringfilter
def esvapi(value, args=''):
    """
    Use ESV API to get a Bible Passage
    http://www.esvapi.org/v2/rest/passageQuery?key=IP&passage=Gen+1:5-10&output-format=plain-text

    Looking for [[bible PASSAGE]]
    
    Usage::
    
        {{ text|esv}}
        {{ text|esv:"option1:value,option2:value"}}
    """
    if BIBLE_RE.search(value) is None:
        return value
    esv_dict = ESV_DICT.copy()
    esv_args = args.split(',')
    if len(esv_args) > 0:
        for arg in esv_args:
            try:
                key, val = arg.split(':')
                if esv_dict.has_key(key):
                    esv_dict[key] = val
            except ValueError:
                pass
    global ESV_QUERY_URL
    ESV_QUERY_URL = ESV_API_URL+'&'.join([k+'='+urllib.quote(str(v)) for (k,v) in esv_dict.items()])
    return BIBLE_RE.sub(_get_esv_txt, value)
esvapi.is_safe = True

def _get_esv_txt(matchObj):
    passage = matchObj.group(1)
    try:
        return markdown.markdown(
            urllib.urlopen(ESV_QUERY_URL+'&'+ESV_QUERY_METHOD+'='+urllib.quote(passage)).read()
        )
    except IOError:
        return passage

@register.filter(name='markdown')
@stringfilter
def markdowner(value, arg=''):
    """
    Filter to create HTML out of Markdown, using custom extensions.

    The diffrence between this filter and the django-internal markdown
    filter (located in ``django/contrib/markup/templatetags/markup.py``)
    is that this filter enables extensions to be load.

    Usage::

        {{ object.text|markdown }}
        {{ object.text|markdown:"save" }}
        {{ object.text|markdown:"codehilite" }}
        {{ object.text|markdown:"save,codehilite" }}

    This code is taken from
    http://www.freewisdom.org/projects/python-markdown/Django
    """
    extensions=arg.split(",")
    if len(extensions) > 0 and extensions[0] == "safe" :
        extensions = extensions[1:]
        safe_mode = True
    else :
        safe_mode = False
    return markdown.markdown(value, extensions, safe_mode=safe_mode)
