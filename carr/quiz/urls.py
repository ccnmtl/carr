import os.path
from django.urls import re_path
from .views import (
    edit_quiz, loadstate, savestate, edit_answer, delete_answer,
    edit_question, delete_question, reorder_questions,
    reorder_answers, add_question_to_quiz, add_answer_to_question,
)

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    re_path(r'^edit_quiz/(?P<id>\d+)/$', edit_quiz, {}, 'edit-quiz'),
    re_path(r'^edit_quiz/(?P<id>\d+)/add_question/$', add_question_to_quiz, {},
            'add-question-to-quiz'),
    re_path(r'^edit_question/(?P<id>\d+)/$', edit_question, {},
            'edit-question'),
    re_path(r'^edit_question/(?P<id>\d+)/add_answer/$', add_answer_to_question,
            {}, 'add-answer-to-question'),
    re_path(r'^delete_question/(?P<id>\d+)/$', delete_question, {},
            'delete-question'),
    re_path(r'^reorder_answers/(?P<id>\d+)/$', reorder_answers, {},
            'reorder-answer'),
    re_path(r'^reorder_questions/(?P<id>\d+)/$', reorder_questions, {},
            'reorder-questions'),
    re_path(r'^delete_answer/(?P<id>\d+)/$', delete_answer, {},
            'delete-answer'),
    re_path(r'^edit_answer/(?P<id>\d+)/$', edit_answer, {}, 'edit-answer'),
    re_path(r'^load/$', loadstate),
    re_path(r'^save/$', savestate),
]
