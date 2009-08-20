from django.contrib.flatpages.models import FlatPage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.template import TemplateDoesNotExist
from django.template.context import get_standard_processors

from utils import get_template

DEFAULT_TEMPLATE = 'flatpages/default.html'

def flatpage(request, url):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(FlatPage, url__exact=url, sites__id__exact=settings.SITE_ID)
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = f.template_name
    else:
        t = DEFAULT_TEMPLATE

    response = render_to_response(t.name, { 'flatpage': f }, request)
    populate_xheaders(request, response, FlatPage, f.id)
    return response
