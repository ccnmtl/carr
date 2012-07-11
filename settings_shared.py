# Django settings for carr project.
import os.path
import re

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'carr' # Or path to database file if using sqlite3.
DATABASE_USER = 'pusher'             # Not used with sqlite3.
DATABASE_USER = 'eddie'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

#For now turn off caching
CACHE_BACKEND = 'locmem://'
#CACHE_BACKEND = 'dummy://'


TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False


MEDIA_ROOT = '/var/www/carr/uploads/'
MEDIA_URL = '/site_media/uploads/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'courseaffils.middleware.CourseManagerMiddleware',
    'someutils.AuthRequirementMiddleware',
    'djangohelpers.middleware.HttpDeleteMiddleware',
)

ROOT_URLCONF = 'carr.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Put application templates before these fallback ones:
    "/var/www/carr/templates/",
    os.path.join(os.path.dirname(__file__),"templates"),
)

INSTALLED_APPS = (
    'activity_bruise_recon',           
    'activity_taking_action',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'pageblocks',
    'pagetree',
    'carr_main',
    'quiz',
    'smartif',
    'sorl.thumbnail',
    'template_utils',
    'tinymce',
    'typogrify',
    'courseaffils',
    'deploy_specific',
    'django_statsd',
    'south'
)

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'carr'
STATSD_HOST = 'localhost'
STATSD_PORT = 8125
STATSD_PATCHES = ['django_statsd.patches.db', ]


THUMBNAIL_SUBDIR = "thumbs"

# for AuthRequirementMiddleware. this should be a list of 
# url prefixes for paths that can be accessed by anonymous
# users. we need to allow anonymous access to the login
# page, and to static resources.

ANONYMOUS_PATHS = ('/accounts/',
                   '/site_media/',
                   '/admin/',
                   '/login/',
                   '/carr/',
                   '/_stats/',
                   re.compile(r'^/$'),
                   )

COURSEAFFILS_PATHS = (
                      #'/carr/',
                      #'/activity/',
                      #re.compile(r'^/$'),
                      )

NON_ANONYMOUS_PATHS = COURSEAFFILS_PATHS

COURSEAFFILS_EXEMPT_PATHS = ANONYMOUS_PATHS
COURSEAFFIL_AUTO_MAP_GROUPS = ['demo']


DEFAULT_SOCIALWORK_FACULTY_USER_IDS = [ 14,  21, 30,   40,  41,  43,  44, 144,  456, 457 ]


# WIND settings
AUTHENTICATION_BACKENDS = ('djangowind.auth.WindAuthBackend','django.contrib.auth.backends.ModelBackend',)


# Pageblocks/Pagetree settings 
PAGEBLOCKS = ['pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'carr_main.PullQuoteBlock_2',
              'carr_main.PullQuoteBlock_3',
              'pageblocks.ImageBlock',
              'carr_main.FlashVideoBlock',
              'quiz.Quiz',
              'activity_bruise_recon.Block',           
              'activity_taking_action.Block',
              #'activity_treatment_choice.Block',
              #'activity_prescription_writing.Block',
              #this appears to be breaking stuff:
              #'carr_main.FlashVideoBlock'
              ] 


#if you add a 'deploy_specific' directory                                                                            
#then you can put a settings.py file and templates/ overrides there            
try:
    from deploy_specific.settings import *
    if locals().has_key('EXTRA_INSTALLED_APPS'):
        INSTALLED_APPS = EXTRA_INSTALLED_APPS + INSTALLED_APPS
except ImportError:
    pass


MANAGERS = ADMINS
