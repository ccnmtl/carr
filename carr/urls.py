import os.path

from django.conf import settings
from django.contrib import admin

import carr.carr_main.views as main_views
from carr.quiz.scores import PostTestAnalysisView
import carr.quiz.scores as scores_views
import carr.quiz.views as quiz_views
from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.generic import TemplateView
import django.views.static
from django_cas_ng import views as cas_views


admin.autodiscover()
site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = [

    path('accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(), name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path('welcome/', RedirectView.as_view(url='/carr')),
    path('crossdomain.xml', django.views.static.serve,
         {'document_root': os.path.abspath(os.path.dirname(__file__)),
          'path': 'crossdomain.xml'}),
    path('', main_views.index),
    path('activity/bruise_recon/',
         include('carr.activity_bruise_recon.urls')),
    path('activity/taking_action/',
         include('carr.activity_taking_action.urls')),

    # ADDING NEW SCORE PAGES JUNE 2012:
    path('scores', scores_views.scores_index),
    # honi soit qui mal y pense
    path('scores/', scores_views.scores_index),
    path('scores/socialwork', scores_views.scores_index),

    path('scores/socialwork/analysis/',
         PostTestAnalysisView.as_view(), name='post-test-analysis'),

    # a list of years
    path('scores/socialwork/year/', scores_views.socialwork_overview),

    # a list of semesters for each year
    re_path(r'^scores/socialwork/year/(?P<year>\d+)/$',
            scores_views.semesters_by_year),

    # a list of classes for each semester
    re_path(r'^scores/socialwork/year/(?P<year>\d+)/semester/(?P<semester>\w+)/$',
            scores_views.classes_by_semester),

    # a student wants to see his or her own scores:
    path('scores/student/',
         scores_views.scores_student, name='student-scores'),

    # a list of students for each class
    re_path((r'^scores/socialwork/course/(?P<c1>\w+)/(?P<c2>\w+)/'
             r'(?P<c3>\w+)/(?P<c4>\w+)/(?P<c5>\w+)/(?P<c6>\w+)/$'),
            scores_views.students_by_class),

    # student lookup by uni -- form
    path('scores/socialwork/uni/', scores_views.student_lookup_by_uni_form),

    path('scores/access/', scores_views.access_list),

    # a faculty member wants to see the score of a student:
    re_path(r'^activity/quiz/studentquiz/(?P<quiz_id>\d+)/user/(?P<user_id>\d+)/$',
            quiz_views.studentquiz),

    # adding classes:
    path('add_classes/', main_views.add_classes),

    # this includes all the quiz stuff, including old urls.
    path('activity/quiz/', include('carr.quiz.urls')),
    path('admin/', admin.site.urls),

    re_path(r'^selenium/(?P<task>\w+)/$', main_views.selenium),

    re_path(r'^stats/(?P<task>\w+)/$', main_views.stats),

    re_path(r'^background/(?P<content_to_show>\w+)/$', main_views.background),

    path('_impersonate/', include('impersonate.urls')),

    path('pagetree/', include('pagetree.urls')),

    path('lti/', include('lti_provider.urls')),

    # analytics:
    path('_stats/', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    re_path(r'^uploads/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT}),

    # very important that this stays last and in this order
    re_path(r'^edit/(?P<path>.*)$', main_views.edit_page),
    re_path(r'^(?P<path>.*)$', main_views.page),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
