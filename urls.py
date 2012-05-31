from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',

   (r'^welcome/$', 'django.views.generic.simple.redirect_to', {'url': '/carr'}),   
   (r'^crossdomain.xml$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.dirname(__file__)), 'path': 'crossdomain.xml'}),
   (r'^$','carr_main.views.index'),
   (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html'}),
   (r'^admin/pagetree/',include('pagetree.urls')),
   (r'^main/', include('carr_main.urls')),
   (r'^activity/bruise_recon/',  include('carr.activity_bruise_recon.urls')),
   (r'^activity/taking_action/', include('carr.activity_taking_action.urls')),
   (r'^activity/quiz/', include('carr.quiz.urls')),
   ('^accounts/',include('djangowind.urls')),
   (r'^admin/', include(admin.site.urls)),
   
   (r'^selenium/(?P<task>\w+)/$', 'carr_main.views.selenium'),
   (r'^stats/(?P<task>\w+)/$', 'carr_main.views.stats'),
   
   (r'^background/(?P<content_to_show>\w+)/$', 'carr_main.views.background'),
   
   (r'^_stats/',direct_to_template, {'template': 'stats.html'}),
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
   (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
   # very important that this stays last and in this order
   (r'^(?P<path>.*)$','carr_main.views.page'),
)
