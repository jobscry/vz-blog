# -*- mode: python; coding: utf-8; -*-
# Django settings for blog project.

import os.path
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'blog.urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_DIR, 'templates'),
	os.path.join(PROJECT_DIR, 'posts', 'templates'),
	os.path.join(PROJECT_DIR, 'users', 'templates'),
	os.path.join(PROJECT_DIR, 'links', 'templates'),
	os.path.join(PROJECT_DIR, 'utils', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
	'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',

)

AUTH_PROFILE_MODULE = 'users.profile'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'blog.utils.context_processors.base_url',
    'blog.utils.context_processors.flatpage_list',
    'blog.utils.context_processors.blog_info',
    'blog.utils.context_processors.google_analytics_js',
)
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'
LOGIN_URL = '/login/'
DATE_FORMAT = 'N j, Y'
DATETIME_FORMAT = 'N j, Y, P'
DEFAULT_CHARSET = 'utf-8'
FORCE_SCRIPT_NAME = ''

INSTALLED_APPS += (
    'tagging',
    'compressor',
    'users',
    'posts',
    'links',
    'stream',
    'django_extensions',
    'south',
)

CACHE_BACKEND = ''
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 60 * 15

BLOG_TITLE = 'test blog'
BLOG_TAGLINE = 'my thoughts and other miscellany'
BLOG_COPYRIGHT = ''
BLOG_COPYRIGHT_URL = ''
BLOG_CODE_URL = ''
POSTS_PER_PAGE = 15
POST_PREVIEW_LENGTH = 200
BLOG_NOTIFY_ON_COMMENT = True

EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
SEND_BROKEN_LINK_EMAILS = True

EXTRA_META = ()
GOOGLE_ANALYTICS_JS = ''
FEEDBURNER_URL = ''

DISQUS = False
DISQUS_IFRAME = ""
DISQUS_JS = ""
