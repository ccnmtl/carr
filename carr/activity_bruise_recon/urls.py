import os.path
import django.views.static

from django.conf.urls import url
from .views import LoadStateView, SaveStateView, StudentView

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),
    url(r'^load/$', LoadStateView.as_view()),
    url(r'^save/$', SaveStateView.as_view()),
    url(r'^studentcase/(?P<block_id>\d+)/user/(?P<user_id>\d+)/$',
        StudentView.as_view()),
]
