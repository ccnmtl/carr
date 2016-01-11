from settings_shared import *  # noqa
from ccnmtlsettings.production import common

locals().update(
    common(
        project=project,
        base=base,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
    ))

try:
    from local_settings import *  # noqa
except ImportError:
    pass
