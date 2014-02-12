# Django settings for carr project.
import os.path
import re
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'carr',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

ALLOWED_HOSTS = [".ccnmtl.columbia.edu", "localhost", ]

ADMINS = ()

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

SOUTH_TESTS_MIGRATE = False

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=carr',
]


# For now turn off caching
CACHE_BACKEND = 'locmem://'
#CACHE_BACKEND = 'dummy://'


TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False


MEDIA_ROOT = '/var/www/carr/uploads/'
MEDIA_URL = '/site_media/uploads/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'courseaffils.middleware.CourseManagerMiddleware',
    'carr.someutils.AuthRequirementMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'djangohelpers.middleware.HttpDeleteMiddleware',
)

ROOT_URLCONF = 'carr.urls'

TEMPLATE_DIRS = (
    "/var/www/carr/carr/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'carr.activity_bruise_recon',
    'carr.activity_taking_action',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'pageblocks',
    'pagetree',
    'carr.carr_main',
    'carr.quiz',
    'smartif',
    'sorl.thumbnail',
    'template_utils',
    'typogrify',
    'courseaffils',
    'django_statsd',
    'south',
    'django_nose',
    'django_jenkins',
    'smoketest',
    'waffle',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = [
    'carr.carr_main',
    'carr.activity_bruise_recon',
    'carr.activity_taking_action',
    'carr.quiz',
]

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
    # re.compile(r'^/$'),
)

NON_ANONYMOUS_PATHS = COURSEAFFILS_PATHS

COURSEAFFILS_EXEMPT_PATHS = ANONYMOUS_PATHS
COURSEAFFIL_AUTO_MAP_GROUPS = ['demo']

DEFAULT_SOCIALWORK_FACULTY_USER_IDS = [
    14,
    21,
    30,
    41,
    44,
    456,
    1514,
    1515,
    1516]

WIND_BASE = "https://wind.columbia.edu/"
WIND_SERVICE = "cnmtl_full_np"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = [
    'djangowind.auth.AffilGroupMapper', 'djangowind.auth.StaffMapper',
    'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', 'jb2410', 'zm4', 'sld2131']

# WIND settings
AUTHENTICATION_BACKENDS = (
    'djangowind.auth.WindAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Pageblocks/Pagetree settings
PAGEBLOCKS = ['pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'carr_main.PullQuoteBlock_2',
              'carr_main.PullQuoteBlock_3',
              'pageblocks.ImageBlock',
              'carr.carr_main.FlashVideoBlock',
              'carr.quiz.Quiz',
              'activity_bruise_recon.Block',
              'activity_taking_action.Block',
              ]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

SITE_ID = 1
MANAGERS = ADMINS

SECRET_KEY = 'dummy'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
