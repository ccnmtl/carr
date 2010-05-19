from models import Quiz, Question, Answer, ActivityState
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from pagetree.models import Hierarchy
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.auth.models import User
import pdb


#import django-courseaffils

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

def get_hierarchy():
    return Hierarchy.objects.get_or_create(name="main",defaults=dict(base_url="/"))[0]

@rendered_with('quiz/edit_quiz.html')
def edit_quiz(request,id):
    quiz = get_object_or_404(Quiz,id=id)
    section = quiz.pageblock().section
    h = get_hierarchy()
    return dict(quiz=quiz,section=section,
                root=h.get_root())

def delete_question(request,id):
    question = get_object_or_404(Question,id=id)
    if request.method == "POST":
        quiz = question.quiz
        question.delete()
        return HttpResponseRedirect(reverse("edit-quiz",args=[quiz.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")

def delete_answer(request,id):
    answer = get_object_or_404(Answer,id=id)
    if request.method == "POST":
        question = answer.question
        answer.delete()
        return HttpResponseRedirect(reverse("edit-question",args=[question.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")


def reorder_answers(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this")
    question = get_object_or_404(Question,id=id)
    keys = request.GET.keys()
    keys.sort()
    answers = [int(request.GET[k]) for k in keys if k.startswith('answer_')]
    question.update_answers_order(answers)
    return HttpResponse("ok")

def reorder_questions(request,id):
    if request.method != "POST":
        return HttpResponse("only use POST for this")
    quiz = get_object_or_404(Quiz,id=id)
    keys = request.GET.keys()
    keys.sort()
    questions = [int(request.GET[k]) for k in keys if k.startswith('question_')]
    quiz.update_questions_order(questions)
    return HttpResponse("ok")

def add_question_to_quiz(request,id):
    quiz = get_object_or_404(Quiz,id=id)
    form = quiz.add_question_form(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        question.ordinality = quiz.question_set.count() + 1
        question.save()
    return HttpResponseRedirect(reverse("edit-quiz",args=[quiz.id]))

@rendered_with('quiz/edit_question.html')
def edit_question(request,id):
    question = get_object_or_404(Question,id=id)
    return dict(question=question)

def add_answer_to_question(request,id):
    question = get_object_or_404(Question,id=id)
    form = question.add_answer_form(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.ordinality = question.answer_set.count() + 1
        answer.save()
    return HttpResponseRedirect(reverse("edit-question",args=[question.id]))

#@rendered_with('quiz/scores.html')
#@rendered_with('quiz/edit_answer.html')

def score_on_quiz (the_quiz, the_student):
    blarg = Question.objects.filter(quiz = the_quiz)
    print blarg       
    #pdb.set_trace()
    #pdb.set_trace()
    try:
        state = ActivityState.objects.get(user=the_student)
        print state.json
        if 1 == 0:
                        if (len(state.json) > 0):
                            score = simplejson.loads (state.json)['question']
                            results = [{
                                        'question':         int(a['id']), 
                                        'actual_answer':    int(a['answer']),
                                        'correct_answer':   answer_key[int(a['id'])],
                                        'quiz_number':      quiz_key  [int(a['id'])]
                            } for a in score]

                            quiz_scores = []
                            
                            for quiz in quizzes:
                                answer_count = len([a for  a in results if a['quiz_number'] == quiz.id ])
                                if answer_count:                
                                    correct_answer_count = len([a for  a in results if a['correct_answer'] == a['actual_answer'] and a['quiz_number'] == quiz.id ])
                                    quiz_scores.append( { 'quiz': quiz, 'score': correct_answer_count, 'answer_count' : answer_count})
                            scores.append( {
                                'student': student,
                                'quiz_scores': quiz_scores,
                                'taking_courses' : taking_courses,
				                'teaching_courses': teaching_courses
                            })
                            
    except:
        pass    




@rendered_with('quiz/scores.html')
def scores(request):
    """
    instructors should be able to view scores for their current students
    admins should be able to view scores for all students ever
    sortable by name, grade, semester, year, instructor would be ideal
    """
    scores = []
    #pdb.set_trace()
    
    
    #get students from request.user
    #if admin:
    #    students = User.objects.all()    
    students = User.objects.all()
    questions = Question.objects.all()
    quizzes = Quiz.objects.all()
    
    #TODO: accept quiz ID as an argument.          
    #pdb.set_trace()

	#SEE  http://www.columbia.edu/acis/rad/authmethods/auth-affil
    # see http://www.columbia.edu/acis/rad/authmethods/wind/ar01s06.html
    quiz_key = {}
    answer_key = {}
    
    for question in questions:
        try:
            answer_key [question.id ] = question.answer_set.get(correct=True).id 
            quiz_key [question.id ] = question.quiz.id
        except:
            pass

    for student in students:
		#note
		# t1.y2010 is fall 2010
		# t3.y2010 is spring 2010
        taking_courses = [x.name for x in student.groups.all() if 'st.course' in x.name and 't3.y2010' in x.name ]
        teaching_courses = [x.name for x in student.groups.all() if 'fc.course' in x.name and 't3.y2010' in x.name ]
        
        #pdb.set_trace()
        try:
            state = ActivityState.objects.get(user=student)
            if (len(state.json) > 0):
                score = simplejson.loads (state.json)['question']
                results = [{
                            'question':         int(a['id']), 
                            'actual_answer':    int(a['answer']),
                            'correct_answer':   answer_key[int(a['id'])],
                            'quiz_number':      quiz_key  [int(a['id'])]
                } for a in score]

                quiz_scores = []
                
                for quiz in quizzes:
                    answer_count = len([a for  a in results if a['quiz_number'] == quiz.id ])
                    if answer_count:                
                        correct_answer_count = len([a for  a in results if a['correct_answer'] == a['actual_answer'] and a['quiz_number'] == quiz.id ])
                        quiz_scores.append( { 'quiz': quiz, 'score': correct_answer_count, 'answer_count' : answer_count})
                scores.append( {
                    'student': student,
                    'quiz_scores': quiz_scores,
                    'taking_courses' : taking_courses,
					'teaching_courses': teaching_courses
                })
                
        except:
            pass
        
         
    return { 'scores':  scores, 'quizzes':quizzes}



@rendered_with('quiz/scores_student.html')
def scores_student(request):
    print score_on_quiz (Quiz.objects.all()[2], request.user)
    return {}

@rendered_with('quiz/scores_faculty.html')
def scores_faculty(request):
    return {}

@rendered_with('quiz/scores_admin.html')
def scores_admin(request):
    return {}


if 1 == 0:
	new_stuff = """
               (r'^scores/$', 'carr.quiz.views.scores'), #this is just temporary for testing.
               (r'^scores/student/$', 'carr.quiz.views.scores_student'),
               (r'^scores/faculty/$', 'carr.quiz.views.scores_faculty'),
               (r'^scores/admin/$', 'carr.quiz.views.scores_admin')"""





@rendered_with('quiz/edit_answer.html')
def edit_answer(request,id):
    answer = get_object_or_404(Answer,id=id)
    return dict(answer=answer)

@login_required
def loadstate(request):
    try: 
        state = ActivityState.objects.get(user=request.user)
        if (len(state.json) > 0):
            doc = state.json
    except ActivityState.DoesNotExist:
        doc = "{}"

    response = HttpResponse(doc, 'application/json')
    response['Cache-Control']='max-age=0,no-cache,no-store'
    return response
    
@login_required
def savestate(request):
    json = request.POST['json']
    try: 
        state = ActivityState.objects.get(user=request.user)
        state.json = json
        state.save()
    except ActivityState.DoesNotExist:
        state = ActivityState.objects.create(user=request.user, json=json)
        
    response = {}
    response['success'] = 1
        
    return HttpResponse(simplejson.dumps(response), 'application/json')
