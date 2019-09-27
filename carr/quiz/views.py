import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from pagetree.helpers import get_hierarchy

from carr.carr_main.models import user_type
from carr.utils import state_json
from carr.quiz.models import Quiz, Question, Answer, ActivityState
from carr.quiz.scores import scores_student


@login_required
def studentquiz(request, quiz_id, user_id):
    """allows a faculty member to see the answers a student posted for a quiz.
    URL, btw, is: /activity/quiz/studentquiz/2/user/5/ """
    template_name = 'quiz/studentquiz.html'
    if user_type(request.user) == 'student':
        return scores_student(request)

    student = get_object_or_404(User, id=user_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    return render(request, template_name, {
        'student': student,
        'quiz': quiz,
        'student_json': state_json(ActivityState, student)
    })


def edit_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    section = quiz.pageblock().section
    h = get_hierarchy()
    return render(request, 'quiz/edit_quiz.html',
                  dict(quiz=quiz, section=section,
                       root=h.get_root()))


def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        quiz = question.quiz
        question.delete()
        return HttpResponseRedirect(reverse("edit-quiz", args=[quiz.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")


def delete_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    if request.method == "POST":
        question = answer.question
        answer.delete()
        return (
            HttpResponseRedirect(reverse("edit-question", args=[question.id]))
        )
    return HttpResponse("""
<html><body><form action="." method="post">Are you sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")


def reorder_answers(request, id):
    if request.method != "POST":
        return HttpResponseForbidden()
    question = get_object_or_404(Question, id=id)
    keys = sorted(request.GET.keys())
    answers = [int(request.GET[k]) for k in keys if k.startswith('answer_')]
    question.update_answers_order(answers)
    return HttpResponse("ok")


def reorder_questions(request, id):
    if request.method != "POST":
        return HttpResponseForbidden()
    quiz = get_object_or_404(Quiz, id=id)
    keys = sorted(request.GET.keys())
    questions = [int(request.GET[k])
                 for k in keys if k.startswith('question_')]
    quiz.update_questions_order(questions)
    return HttpResponse("ok")


def add_question_to_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    form = quiz.add_question_form(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        question.ordinality = quiz.question_set.count() + 1
        question.save()
    return HttpResponseRedirect(reverse("edit-quiz", args=[quiz.id]))


def edit_question(request, id):
    question = get_object_or_404(Question, id=id)
    return render(request, 'quiz/edit_question.html', dict(question=question))


def add_answer_to_question(request, id):
    question = get_object_or_404(Question, id=id)
    form = question.add_answer_form(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.ordinality = question.answer_set.count() + 1
        answer.save()
    return HttpResponseRedirect(reverse("edit-question", args=[question.id]))


def edit_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    return render(request, 'quiz/edit_answer.html', dict(answer=answer))


@login_required
def loadstate(request):
    response = HttpResponse(state_json(ActivityState, request.user),
                            'application/json')
    response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return response


@login_required
def savestate(request):
    jsn = request.POST['json']
    try:
        state = ActivityState.objects.get(user=request.user)
        state.json = jsn
        state.save()
    except ActivityState.DoesNotExist:
        state = ActivityState.objects.create(user=request.user, json=jsn)

    response = {}
    response['success'] = 1

    return HttpResponse(json.dumps(response), 'application/json')
