# -*- mode: python; coding: utf-8; -*-
# http://bretthoerner.com/blog/2008/oct/27/using-nginx-memcached-module-django/

from django.conf import settings
from django.core.cache import cache

KEY = getattr(settings, 'NGINX_CACHE_PREFIX', 'NG')

class NginxMemcacheMiddleWare:
    def process_response(self, request, response):

        path = request.get_full_path()

        if request.method != "GET" \
           or (path.startswith('/admin') and not request.user.is_anonymous()) \
           or response.status_code != 200:
            return response

        # settings.NGINX_CACHE_PREFIX == 'NG', just like nginx.conf
        key = "%s:%s" % (KEY, path)
        cache.set(key, response.content)

        return response
