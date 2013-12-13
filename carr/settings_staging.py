# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/carr/carr/carr/templates",
)

MEDIA_ROOT = '/var/www/carr/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/carr/carr/media'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'carr',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/carr/carr/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
STAGING_ENV = True

STATSD_PREFIX = 'carr-staging'
SENTRY_SITE = 'carr-staging'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
STATICFILES_DIRS = ()

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django')

    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
