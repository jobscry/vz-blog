import re
import time
import datetime

from django import forms
from django.forms import ModelForm
from django.forms.util import ErrorDict
from django.conf import settings
from django.http import Http404
from django.utils.encoding import force_unicode
from django.utils.hashcompat import sha_constructor
from posts.models import Post

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class SearchForm(forms.Form):
	search_string = forms.CharField(max_length=100, label='Look for')

class MarkItUpWidget(forms.Textarea):
    class Media:
        js = (
            'js/jquery.js',
            'js/markitup/jquery.markitup.js',
            'js/markitup/sets/markdown/set.js',
            'js/markitup.js',
        )
        css = {
            'screen': (
                'js/markitup/skins/markitup/style.css',
                'js/markitup/sets/markdown/style.css',
            )
        }

class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=MarkItUpWidget())

    class Meta:
        model = Post
