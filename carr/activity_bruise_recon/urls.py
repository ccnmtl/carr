from django.conf.urls import patterns
import os.path
from .views import LoadStateView, SaveStateView

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'^load/$', LoadStateView.as_view()),
    (r'^save/$', SaveStateView.as_view()),
    (r'^studentcase/(?P<block_id>\d+)/user/(?P<user_id>\d+)/$',
     'carr.activity_bruise_recon.views.student'),
)
