# flake8: noqa

# Django settings for carr project.
import os.path
import re
import sys
from datetime import timedelta

from ccnmtlsettings.shared import common
project = 'carr'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'carr',
    }
}
if 'test' in sys.argv or 'jenkins' in sys.argv:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            'LOCATION': 'carr',
        }
    }


MIDDLEWARE += [  # noqa
    'courseaffils.middleware.CourseManagerMiddleware',
    'carr.someutils.AuthRequirementMiddleware',
    'djangohelpers.middleware.HttpDeleteMiddleware',
    'carr.middleware.SiteIdMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware'
]

INSTALLED_APPS += [  # noqa
    'carr.activity_bruise_recon',
    'carr.activity_taking_action',
    'pageblocks',
    'pagetree',
    'carr.carr_main',
    'carr.quiz',
    'sorl.thumbnail',
    'courseaffils',
    'bootstrap3',
    'lti_provider'
]

PROJECT_APPS = [
    'carr.carr_main',
    'carr.activity_bruise_recon',
    'carr.activity_taking_action',
    'carr.quiz',
]

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
)

NON_ANONYMOUS_PATHS = COURSEAFFILS_PATHS

COURSEAFFILS_EXEMPT_PATHS = ANONYMOUS_PATHS
COURSEAFFIL_AUTO_MAP_GROUPS = ['demo']

DEFAULT_SOCIALWORK_FACULTY_UNIS = [
    'amo1', 'dls3', 'vc2162', 'jkt4', 'hh2537', 'mj52'
]

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

SITE_ID = 1
SITE_DENTAL = 1
SITE_SOCIAL_WORK = 2

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'carr.carr_main.views.context_processor',
)

AUTHENTICATION_BACKENDS = [
  'django.contrib.auth.backends.ModelBackend',
  'lti_provider.auth.LTIBackend',
  'djangowind.auth.SAMLAuthBackend'
]

LTI_TOOL_CONFIGURATION = {
    'title': 'Child Abuse Reporting Education',
    'description': 'An online resource to teach students how to recognize'
    'the symptoms of child abuse and how to report abuse when acting in their'
    'professional capacities.',
    'launch_url': 'lti/',
    'embed_url': '',
    'embed_icon_url': '',
    'embed_tool_id': '',
    'landing_url': '{}://{}/',
    'course_aware': False,
    'navigation': False,
    'new_tab': True,
    'frame_width': 1024,
    'frame_height': 1024
}
