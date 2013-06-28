# -*- coding: utf-8 -*-
import os

from sys import path


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
OPENSHIFT_DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', '') or PACKAGE_ROOT

path.append(PROJECT_ROOT)
path.append(os.path.join(PROJECT_ROOT, "apps"))

# a setting to determine whether we are running on OpenShift
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    DEBUG = os.environ.get("DEBUG", "").lower() in ("true", "1", "on") or False
    TEMPLATE_DEBUG = DEBUG
    REMOTE_STORAGE = True
    THUMBNAIL_DEBUG = False
    THUMBNAIL_CACHE_TIMEOUT = 3600 * 24 * 365 # 365 dias
else:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    REMOTE_STORAGE = bool(os.environ.get('REMOTE_STORAGE', '').lower() in ['1', 'true', 'on'])
    THUMBNAIL_DEBUG = bool(os.environ.get('THUMBNAIL_DEBUG', '').lower() in ['1', 'true', 'on'])
    THUMBNAIL_DUMMY = bool(os.environ.get('THUMBNAIL_DUMMY', '1').lower() in ['1', 'true', 'on'])


ADMINS = [
]

MANAGERS = ADMINS

if ON_OPENSHIFT:
    DATABASES = {
        "default": {
            "ENGINE": "django_mysqlpool.backends.mysqlpool",
            "NAME": "dbname",
            "USER": "user",
            "PASSWORD": "passw",
            "HOST": "",
            "PORT": "",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django_mysqlpool.backends.mysqlpool",
            "NAME": "clean_orchids",
            "PASSWORD": "user",
            "USER": "passw",
            "HOST": "",
            "PORT": "",
        }
    }

MYSQLPOOL_BACKEND = 'QueuePool'
MYSQLPOOL_ARGUMENTS = {
    'use_threadlocal': False,
}

SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.mysql'}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

# use local site
SITE_ID = 1
if ON_OPENSHIFT:
    # use production site
    SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(OPENSHIFT_DATA_DIR, "site_media", "media")
#os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(OPENSHIFT_DATA_DIR, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "&amp;o=23^3(ow8bobhj^u-jqdop!^@4k%1ry-1eu505#pr-e!$_hk"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "pinax_utils.context_processors.settings",
    "account.context_processors.account",
    "orcheeder.context_processors.search_form",
]

# redirect to www.orcheeder.com when orcheeder.com
# so we dont have duplicated urls
PREPEND_WWW = True

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    'django.middleware.gzip.GZipMiddleware',
    "orcheeder.middlewares.SpacelessMiddleware",
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'waffle.middleware.WaffleMiddleware',
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "johnny.middleware.LocalStoreClearMiddleware",
    "johnny.middleware.QueryCacheMiddleware",
]

if not ON_OPENSHIFT and DEBUG:
    MIDDLEWARE_CLASSES += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "orcheeder.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "orcheeder.wsgi.application"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.markup",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    'django.contrib.flatpages',
    "suit",
    "django.contrib.admin",

    # theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",

    # external
    "account",
    "metron",
    "eventlog",
    "south",
    "robots",
    "haystack",
    "disqus",
    "pagination",
    "planet",
    "tagging",
    "memcache_status",
    "sorl.thumbnail",
    "django_extensions",
    "gunicorn",
    "djrill",
    "waffle",
    'raven.contrib.django.raven_compat',

    # project
    "orcheeder",

    # apps
    "taxon",
    "countries",
    "conditions",
    "tips",
    "growers",
]

if not ON_OPENSHIFT and DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

# lo desactive hasta q sepamos q envia mail, pq hay errores y no los veo
if ON_OPENSHIFT:
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = ["localhost:8000", "localhost"]

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

DEFAULT_FROM_EMAIL = ""

AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
]

# DISQUS integration: http://django-disqus.readthedocs.org/en/latest/
DISQUS_API_KEY = ''
DISQUS_WEBSITE_SHORTNAME = ''

# HAYSTACK config:
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
HAYSTACK_ITERATOR_LOAD_PER_QUERY = 60
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = True
HAYSTACK_ID_FIELD = 'id'
HAYSTACK_DJANGO_CT_FIELD = 'django_ct'
HAYSTACK_DJANGO_ID_FIELD = 'django_id'

if ON_OPENSHIFT:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://localhost:9200/',
            'INDEX_NAME': 'orcheeder'
        },
    }
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://localhost:9200/',
            'INDEX_NAME': 'clean_orchids'
        },
    }


# METRON config
METRON_SETTINGS = {
}

# django-planet
PLANET = {"USER_AGENT": "orcheeder/0.1"}

# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TEMPLATE_CONTEXT": True,
    "ENABLE_STACKTRACES": True,
}

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'haystack.panels.HaystackDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

# django-storages: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_QUERYSTRING_AUTH = False
S3_URL = '//domain.cloudfront.net'
AWS_LOCATION = "media"

if not REMOTE_STORAGE:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # serve media and static files from amazon s3
    DEFAULT_FILE_STORAGE = 'orcheeder.custom_storages.MediaS3BotoStorage'
    MEDIA_URL = S3_URL + "/media/"

    STATICFILES_STORAGE = 'orcheeder.custom_storages.StaticS3BotoStorage'
    STATIC_URL = S3_URL + "/static/"

# cache configuration:
if ON_OPENSHIFT:
    CACHES = {
        'default': {
            'BACKEND': 'johnny.backends.memcached.MemcachedCache',
            'LOCATION': os.environ.get("DEFAULT_CACHE_URL", "127.0.0.1:11211"),
            'JOHNNY_CACHE': True,
            'TIMEOUT': 172800,
            'OPTIONS': {
                'MAX_ENTRIES': 500000
            },
            'version': 1
        }
    }
else:
    # use dummy cache for development environment
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'orcheeder-dev',
            'TIMEOUT': 7200,
        }
    }

JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc-orcheeder'
JOHNNY_MIDDLEWARE_SECONDS = 3600 * 24 # 1 dia

# django-robots
ROBOTS_USE_SITEMAP = True
ROBOTS_SITEMAP_URLS = [
    "http://www.orcheeder.com/sitemap.xml",
]

MANDRILL_API_KEY = ""

if ON_OPENSHIFT:
    RAVEN_CONFIG = {
        'dsn': '',
    }
