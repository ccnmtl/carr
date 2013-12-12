from django.conf.urls.defaults import patterns
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'^load/$',
     'carr.activity_taking_action.views.loadstate'),
    (r'^save/$',
     'carr.activity_taking_action.views.savestate'),
    (r'^student/(?P<user_id>\d+)/$',
     'carr.activity_taking_action.views.student'),
)
