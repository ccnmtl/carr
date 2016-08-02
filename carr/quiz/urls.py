from django.conf.urls import url
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^edit_quiz/(?P<id>\d+)/$',
        'carr.quiz.views.edit_quiz', {}, 'edit-quiz'),
    url(r'^edit_quiz/(?P<id>\d+)/add_question/$',
        'carr.quiz.views.add_question_to_quiz', {}, 'add-question-to-quiz'),
    url(r'^edit_question/(?P<id>\d+)/$',
        'carr.quiz.views.edit_question', {}, 'edit-question'),
    url(r'^edit_question/(?P<id>\d+)/add_answer/$',
        'carr.quiz.views.add_answer_to_question', {},
        'add-answer-to-question'),
    url(r'^delete_question/(?P<id>\d+)/$',
        'carr.quiz.views.delete_question', {}, 'delete-question'),
    url(r'^reorder_answers/(?P<id>\d+)/$',
        'carr.quiz.views.reorder_answers', {}, 'reorder-answer'),
    url(r'^reorder_questions/(?P<id>\d+)/$',
        'carr.quiz.views.reorder_questions', {}, 'reorder-questions'),
    url(r'^delete_answer/(?P<id>\d+)/$',
        'carr.quiz.views.delete_answer', {}, 'delete-answer'),
    url(r'^edit_answer/(?P<id>\d+)/$',
        'carr.quiz.views.edit_answer', {}, 'edit-answer'),
    url(r'^load/$', 'carr.quiz.views.loadstate'),
    url(r'^save/$', 'carr.quiz.views.savestate'),
]
