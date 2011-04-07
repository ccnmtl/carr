import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/carr/carr/ve/lib/python2.6/site-packages')

# see http://code.google.com/p/modwsgi/wiki/ApplicationIssues#Writing_To_Standard_Output
sys.stdout = sys.stderr

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/carr/')
sys.path.append('/var/www/carr/carr/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'carr.settings_production_dental'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
