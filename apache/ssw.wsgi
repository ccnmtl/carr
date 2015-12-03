import os, sys, site

# http://bugs.python.org/issue7980
import _strptime

# paths we might need to pick up the project's settings
sys.path.append('/var/www/carr/carr/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'carr.settings_socialwork'

import django.core.handlers.wsgi
import django
django.setup()

application = django.core.handlers.wsgi.WSGIHandler()
