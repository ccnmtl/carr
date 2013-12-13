import os, sys, site

# paths we might need to pick up the project's settings
sys.path.append('/var/www/carr/carr/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'carr.settings_staging'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
