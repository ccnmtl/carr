# flake8: noqa
from carr.settings_shared import *  # noqa
from ccnmtlsettings.production import common
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

locals().update(
    common(
        project=project,
        base=base,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
    ))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

try:
    from carr.local_settings import *  # noqa
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
￼   sentry_sdk.init(
￼       dsn=SENTRY_DSN,
￼       integrations=[DjangoIntegration()],
￼   )
