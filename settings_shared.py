# Django settings for carr project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('CCNMTL', 'ccnmtl-sysadmin@columbia.edu'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'carr' # Or path to database file if using sqlite3.
DATABASE_USER = 'postgres'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
MEDIA_ROOT = "/var/www/carr/uploads/"
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
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
    #'activity_prescription_writing',
    #'activity_treatment_choice',
    #'activity_virtual_patient',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
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
)

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[carr] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "carr@ccnmtl.columbia.edu"

# WIND settings

AUTHENTICATION_BACKENDS = ('djangowind.auth.WindAuthBackend','django.contrib.auth.backends.ModelBackend',)
WIND_BASE = "https://wind.columbia.edu/"
WIND_SERVICE = "cnmtl_full_np"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper','djangowind.auth.StaffMapper','djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8','jb2410','zm4','sbd12','egr2107','kmh2124','sld2131','amm8','mar227','ed2198']

# Pageblocks/Pagetree settings 
PAGEBLOCKS = ['pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'pageblocks.PullQuoteBlock_2',
              'pageblocks.PullQuoteBlock_3',
              'pageblocks.ImageBlock',
              'carr_main.FlashVideoBlock',
              'quiz.Quiz',
              #'activity_treatment_choice.Block',
              #'activity_prescription_writing.Block',
              #this appears to be breaking stuff:
              #'carr_main.FlashVideoBlock'
              ] 
