import os.path
import django.views.static

from django.urls import re_path
from .views import LoadStateView, SaveStateView, StudentView

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': media_root}),
    re_path(r'^load/$', LoadStateView.as_view()),
    re_path(r'^save/$', SaveStateView.as_view()),
    re_path(r'^studentcase/(?P<block_id>\d+)/user/(?P<user_id>\d+)/$',
            StudentView.as_view()),
]
