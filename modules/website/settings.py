# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
import os, sys

# Import Application libraries
sys.path.append('../../../lib/')

# Django settings for website project.
DEBUG = False
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_URL = 'http://www.zaposlim.se'

PREPEND_WWW = True
APPEND_SLASH = True

ADMINS = (
    ('Mitja Kramberger', 'mitja.kramberger@gmail.com'),
    ('Ales Maticic', 'gospodarprstanov@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zaposlim_se',                  # Or path to database file if using sqlite3.
        'USER': 'webapp',                       # Not used with sqlite3.
        'PASSWORD': 'password',            # Not used with sqlite3.
        'HOST': '62.75.139.151',                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                         # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
        }
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sl'
LANGUAGE_COOKIE_NAME = 'zaposlim_lang'

# Available languages
LANGUAGES = (
  ('en', _('English')),
  ('sl', _('Slovene')),
)

# Path to locale files
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, '../conf/locale/'),)
LOCALE_PATH_JS = os.path.join(PROJECT_ROOT, '../conf/locale/')

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.zaposlim.se'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$8t*v@q&p9@41h$jcl90czbe17ilr6dscu%c3e7&$zy=n6ex@@'

# Session cookie domain (make sure you adjust this according to the
# domains/subdomains that you are using!)
SESSION_COOKIE_DOMAIN = 'www.zaposlim.se'
SESSION_COOKIE_NAME = 'zaposlim_auth'
SESSION_COOKIE_AGE = 1209600         # (2 weeks, in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Authentication login/logout urls.
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

# COMPRESS
COMPRESS_OFFLINE = True
COMPRESS_VERSION = True
COMPRESS_ROOT = os.path.join(PROJECT_ROOT, 'static/')
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', '/var/lib/gems/1.8/bin/sass --scss {infile} {outfile}'),
)

# ElasticSearch config
SEARCH_HOSTS = ['62.75.139.151:9200']
SEARCH_WHAT_FIELDS = ['title', 'company.name', 'category', 'summary', 'content']
SEARCH_MIN_QUERY_LENGTH = 3
SEARCH_FACETS_SIZE = 22
SEARCH_ALIASES = [
    'delo',
    'mojazaposlitev',
    'mojedelo',
    'zaposlitev',
    'zavod'
]

# Application setting
APP_SEARCHES_TOP = 11
APP_SEARCHES_LAST = 11
APP_SEARCHES_LENGTH = 28

APP_SEARCHES_MORE_TOP = 75
APP_SEARCHES_MORE_LAST = 75
APP_SEARCHES_MORE_COLUMNS = ['first','second', 'third', 'fourth','fifth']

APP_GEO_CITIES_RANGE = '10km'
APP_GEO_CITIES = {  # Latitude, Longitude
    'ljubljana'     : (46.0514263, 14.5059655),
    'maribor'       : (46.5573993, 15.645982),
    'celje'         : (46.231018,  15.2602936),
    'kranj'         : (46.2392066, 14.3556543),
    'velenje'       : (46.3587118, 15.1080001),
    'koper'         : (45.5482731, 13.731213),
    'novo mesto'    : (45.8041957, 15.1696785),
    'ptuj'          : (46.4199885, 15.8699813),
    'jesenice'      : (46.430556,  14.066944),
    'nova gorica'   : (45.9560428719385, 13.6483669281006),
    'murska sobota' : (46.6625, 16.1663889)
}

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'website.apps.common.context_processors.site',
)

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mail@zaposlim.se'
EMAIL_HOST_PASSWORD = 'delampridno'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Pagination config
PAGINATION_PAGE_SIZE = 12
PAGINATION_CURRENT_LEFT = 6
PAGINATION_CURRENT_RIGHT = 6
PAGINATION_EDGE_LEFT = 2
PAGINATION_EDGE_RIGHT = 2

# File upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520 # 20 MB
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

MIDDLEWARE_CLASSES = (
    'website.apps.crawlable.middleware.CrawlableMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'website.urls'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sessions',
    # lib
    'compressor',
    'djcelery',
    # apps
    'website.apps.api',
    'website.apps.common',
    'website.apps.search',
    'website.apps.search.templatetags',
    'website.apps.crawlable',
)

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [ '62.75.139.151:11211' ],
        'TIMEOUT': 60*60*24, # 1 day
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# backup scrapers
BACKUP_INDICES = '/var/lib/scraper/'

# tor settings
TOR_PASSPHRASE = '16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C'

# Celery
import djcelery
from celery.schedules import crontab

# Broker settings
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "scraper"
BROKER_PASSWORD = "delampridno"
BROKER_VHOST = "webapp"

# Worker settings
CELERY_ACKS_LATE = True

# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True

# Email address used as sender (from field).
SERVER_EMAIL = "mail@zaposlim.se"
CELERY_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Mailserver configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mail@zaposlim.se'
EMAIL_HOST_PASSWORD = 'delampridno'
EMAIL_PORT = 587
EMAIL_USE_SSL = True

# events
CELERY_SEND_EVENTS = True
CELERY_DISABLE_RATE_LIMITS = True

# periodic tasks
CELERYBEAT_SCHEDULE = {
    'renew-tor-every-6-hours': {
        'task': 'website.apps.common.tasks.renewip.RenewIp',
        'schedule': crontab(minute=0, hour="*/6", day_of_week='mon-fri')
    },
    'runs-spiders-every-6-hours': {
        'task': 'website.apps.common.tasks.run.RunSpiders',
        'schedule': crontab(minute=10, hour="*/6", day_of_week='mon-fri')
    },
    'runs-backup-daily-at-midnight': {
        'task': 'website.apps.search.tasks.backup.BackupData',
        'schedule': crontab(minute=0, hour=0, day_of_week='mon-fri')
    }
}

djcelery.setup_loader()

# Piston config
PISTON_EMAIL_ERRORS = True
PISTON_DISPLAY_ERRORS = False

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'console': {
            'format': '%(asctime)s %(levelname)8s %(name)s[%(funcName)s]: %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'ERROR',
    },
}

try:
    from settings_local import *
except ImportError:
    pass
