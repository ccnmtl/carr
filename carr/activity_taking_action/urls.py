from django.conf.urls import patterns
from .views import LoadStateView, SaveStateView, StudentView
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'^load/$', LoadStateView.as_view()),
    (r'^save/$', SaveStateView.as_view()),
    (r'^student/(?P<user_id>\d+)/$', StudentView.as_view()),
)
