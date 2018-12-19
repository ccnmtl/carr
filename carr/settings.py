# flake8: noqa
from carr.settings_shared import *

try:
    from carr.local_settings import *
except ImportError:
    pass
