# Django settings for blog project.

import os.path
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'blog'             # Or path to database file if using sqlite3.
DATABASE_USER = 'blog'             # Not used with sqlite3.
DATABASE_PASSWORD = 'blog'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

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
SECRET_KEY = '7paeceaujt*pl%#_poc0q%74$)j!1d#jmoz)%^r*0d*i$z1znx'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.http.ConditionalGetMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.csrf.middleware.CsrfMiddleware',
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
	os.path.join(PROJECT_DIR, 'stream', 'templates'),
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
    'tagging',
    'timezones',
    'users',
	'posts',
	'links',
	'stream',
)

AUTH_PROFILE_MODULE = 'users.profile'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'blog.utils.context_processors.base_url',
    'blog.utils.context_processors.flatpage_list',
    'blog.utils.context_processors.blog_info',
)
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'
LOGIN_URL = '/login/'
DATE_FORMAT = 'N j, Y'
DATETIME_FORMAT = 'N j, Y, P'
DEFAULT_CHARSET = 'utf-8'
FORCE_SCRIPT_NAME = ''

INSTALLED_APPS += (
    'batchadmin',
    'django_extensions', 
    'django_evolution',
)
BATCHADMIN_MEDIA_PREFIX = 'batch-admin/'

CACHE_BACKEND = ''
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 60 * 15

AKISMET_API_KEY = ''
BLOG_TITLE = 'test blog'
BLOG_TAGLINE = 'my thoughts and other miscellany'
BLOG_COPYRIGHT = ''
BLOG_COPYRIGHT_URL = ''
BLOG_CODE_VERSION = '0.1b'
BLOG_CODE_URL = ''
MAX_COMMENT_DAYS = 60
POSTS_PER_PAGE = 3
POST_PREVIEW_LENGTH = 200
BLOG_NOTIFY_ON_COMMENT = True

EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
SEND_BROKEN_LINK_EMAILS = True
