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
   
   
    #ADDING NEW SCORE PAGES JUNE 2012:
    (r'^scores$',             'carr.quiz.scores.scores_index'),
    (r'^scores/$',            'carr.quiz.scores.scores_index'), #honi soit qui mal y pense
    (r'^scores/socialwork$',  'carr.quiz.scores.scores_index'),
    (r'^scores/socialwork/$', 'carr.quiz.scores.scores_index'),
    
     # a list of years
    (r'^scores/socialwork/year/$', 'carr.quiz.scores.socialwork_overview'),
   
    #a list of semesters for each year
    (r'^scores/socialwork/year/(?P<year>\d+)/$', 'carr.quiz.scores.semesters_by_year'),
   
    # a list of classes for each semester
    (r'^scores/socialwork/year/(?P<year>\d+)/semester/(?P<semester>\w+)/$', 'carr.quiz.scores.classes_by_semester'),
   
    #/scores/socialwork/course/{{c.0}}/{{c.1}}/{{c.2}}/{{c.3}}/{{c.4}}/{{c.5}}/ 
    #/(?P<c1>\w+)/(?P<c2>\w+)/(?P<c3>\w+)/(?P<c4>\w+)/(?P<c5>\w+)/(?P<c6>\w+)/$
   
   #a faculty member wants to see the score of a student:
   (r'^activity/quiz/studentquiz/(?P<quiz_id>\d+)/user/(?P<user_id>\d+)/$', 'carr.quiz.views.studentquiz'),
   
   # a student wants to see his or her own scores:
   (r'^scores/student/$', 'carr.quiz.scores.scores_student'),
   
   
    # a list of students for each class
    (r'^scores/socialwork/course/(?P<c1>\w+)/(?P<c2>\w+)/(?P<c3>\w+)/(?P<c4>\w+)/(?P<c5>\w+)/(?P<c6>\w+)/$', 'carr.quiz.scores.students_by_class'),


    # adding classes:
	(r'^add_classes/$', 'carr.carr_main.views.add_classes'),

    # student lookup by uni -- form
    (r'^scores/socialwork/uni/$', 'carr.quiz.scores.student_lookup_by_uni_form'),

    # student lookup by uni -- results
    # (r'^scores/socialwork/uni/(?P<uni>\w+)/$', 'carr.quiz.scores.student_lookup_by_uni_results'),


   
    #this includes all the quiz stuff, including old urls.   
    (r'^activity/quiz/', include('carr.quiz.urls')),
    ('^accounts/',include('djangowind.urls')),
    (r'^admin/', include(admin.site.urls)),
   
    (r'^selenium/(?P<task>\w+)/$', 'carr_main.views.selenium'),
    
    
    #(r'^stats/(?P<task>\w+)/$', 'carr_main.views.stats_csv'),
   
    (r'^stats/(?P<task>\w+)/$', 'carr_main.views.stats_csv'),
   
   
   
   
    (r'^background/(?P<content_to_show>\w+)/$', 'carr_main.views.background'),
   
   
    #analytics:
    (r'^_stats/',direct_to_template, {'template': 'stats.html'}),
   
   
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
    # very important that this stays last and in this order
    (r'^(?P<path>.*)$','carr_main.views.page'),
)
