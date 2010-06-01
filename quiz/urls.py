from django.conf.urls.defaults import patterns
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
                       (r'^edit_quiz/(?P<id>\d+)/$','quiz.views.edit_quiz',{},'edit-quiz'),
                       (r'^edit_quiz/(?P<id>\d+)/add_question/$','quiz.views.add_question_to_quiz',{},'add-question-to-quiz'),
                       (r'^edit_question/(?P<id>\d+)/$','quiz.views.edit_question',{},'edit-question'),
                       (r'^edit_question/(?P<id>\d+)/add_answer/$','quiz.views.add_answer_to_question',{},'add-answer-to-question'),
                       (r'^delete_question/(?P<id>\d+)/$','quiz.views.delete_question',{},'delete-question'),
                       (r'^reorder_answers/(?P<id>\d+)/$','quiz.views.reorder_answers',{},'reorder-answer'),
                       (r'^reorder_questions/(?P<id>\d+)/$','quiz.views.reorder_questions',{},'reorder-questions'),
                       (r'^delete_answer/(?P<id>\d+)/$','quiz.views.delete_answer',{},'delete-answer'),
                       (r'^edit_answer/(?P<id>\d+)/$','quiz.views.edit_answer',{},'edit-answer'),
                       (r'^load/$', 'carr.quiz.views.loadstate'),
                       (r'^save/$',   'carr.quiz.views.savestate'),
                       #(r'^scores/$', 'carr.quiz.views.scores'), #this is just temporary for testing.
                       
                       
                       
                       (r'^scores/student/$', 'carr.quiz.views.scores_student'),
                       
                       
                       #todo: refactor out.
                       (r'^scores/faculty/$', 'carr.quiz.views.scores_faculty'),
                       
                       #list all courses for the logged-in faculty member.
                       (r'^scores/faculty/courses/$', 'carr.quiz.views.scores_faculty_courses'),
                       
                       
                       #  (?P<game_label>\w+)
                       
                       #  (?P<c1>\w+)

                       #  (?P<c1>\w+)/(?P<c2>\w+)/(?P<c3>\w+)/(?P<c4>\w+)/(?P<c5>\w+)/$
                       



                       
                       #show results for all students in one course.
#                       (r'^scores/faculty/course/(?P<id>\d+)/$', \


                       (r'^scores/faculty/course/(?P<c1>\w+)/(?P<c2>\w+)/(?P<c3>\w+)/(?P<c4>\w+)/(?P<c5>\w+)/(?P<c6>\w+)/$', \
                       'carr.quiz.views.scores_faculty_course'),

                       
                       (r'^scores/admin/$', 'carr.quiz.views.scores_admin')
)
