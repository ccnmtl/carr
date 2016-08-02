import carr.carr_main.views as main_views
import carr.quiz.scores as scores_views
import carr.quiz.views as quiz_views

import django.views.static
import os.path

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic import RedirectView


admin.autodiscover()
site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = [
    url(r'^welcome/$', RedirectView.as_view(url='/carr')),
    url(r'^crossdomain.xml$', django.views.static.serve,
        {'document_root': os.path.abspath(os.path.dirname(__file__)),
         'path': 'crossdomain.xml'}),
    url(r'^$', main_views.index),
    url(r'^logout/$', logout, {'template_name': 'logged_out.html'}),
    url(r'^activity/bruise_recon/',
        include('carr.activity_bruise_recon.urls')),
    url(r'^activity/taking_action/',
        include('carr.activity_taking_action.urls')),

    # ADDING NEW SCORE PAGES JUNE 2012:
    url(r'^scores$', scores_views.scores_index),
    # honi soit qui mal y pense
    url(r'^scores/$', scores_views.scores_index),
    url(r'^scores/socialwork$', scores_views.scores_index),
    url(r'^scores/socialwork/$', scores_views.scores_index),

    # a list of years
    url(r'^scores/socialwork/year/$', scores_views.socialwork_overview),

    # a list of semesters for each year
    url(r'^scores/socialwork/year/(?P<year>\d+)/$',
        scores_views.semesters_by_year),

    # a list of classes for each semester
    url(r'^scores/socialwork/year/(?P<year>\d+)/semester/(?P<semester>\w+)/$',
        scores_views.classes_by_semester),

    # a student wants to see his or her own scores:
    url(r'^scores/student/$', scores_views.scores_student),

    # a list of students for each class
    url((r'^scores/socialwork/course/(?P<c1>\w+)/(?P<c2>\w+)/'
         r'(?P<c3>\w+)/(?P<c4>\w+)/(?P<c5>\w+)/(?P<c6>\w+)/$'),
        scores_views.students_by_class),

    # student lookup by uni -- form
    url(r'^scores/socialwork/uni/$', scores_views.student_lookup_by_uni_form),

    url(r'^scores/access/$', scores_views.access_list),

    # a faculty member wants to see the score of a student:
    url(r'^activity/quiz/studentquiz/(?P<quiz_id>\d+)/user/(?P<user_id>\d+)/$',
        quiz_views.studentquiz),

    # adding classes:
    url(r'^add_classes/$', main_views.add_classes),

    # this includes all the quiz stuff, including old urls.
    url(r'^activity/quiz/', include('carr.quiz.urls')),
    url('^accounts/', include('djangowind.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^selenium/(?P<task>\w+)/$', main_views.selenium),

    url(r'^stats/(?P<task>\w+)/$', main_views.stats),

    url(r'^background/(?P<content_to_show>\w+)/$', main_views.background),

    url(r'^pagetimer/', include('pagetimer.urls')),
    url(r'^pagetree/', include('pagetree.urls')),

    # analytics:
    url(r'^_stats/', TemplateView.as_view(template_name="stats.html")),
    url('^smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    # very important that this stays last and in this order
    url(r'^edit/(?P<path>.*)$', main_views.edit_page),
    url(r'^(?P<path>.*)$', main_views.page),
]
