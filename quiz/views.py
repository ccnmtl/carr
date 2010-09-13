from models import Quiz, Question, Answer, ActivityState
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from pagetree.models import Hierarchy
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.auth.models import User, Group
from activity_bruise_recon.models import ActivityState as bruise_recon_state
from activity_taking_action.models import ActivityState as taking_action_state
from django.contrib.sites.models import Site, RequestSite
from carr_main.models import number_of_students_in_class, students_in_class


from activity_taking_action.models import score_on_taking_action
from activity_bruise_recon.models import score_on_bruise_recon
from django.core.cache import cache

import re, pdb

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

# a couple helper functions for scoring:
def score_on_all_quizzes (the_student):
    tmp = question_and_quiz_keys()
    answer_key = tmp ['answer_key']
    quiz_key =   tmp ['quiz_key']

    questions = Question.objects.all()
    quizzes = Quiz.objects.all()

    #pdb.set_trace()
    try:
        state = ActivityState.objects.get(user=the_student)
        #print state.json
    except ActivityState.DoesNotExist:
        return []
        
    if (len(state.json) > 0):
        score = []
        
        for a in simplejson.loads (state.json).values():
            try:
                score.extend(a['question'])
            except:
                pass #eh.

        # if int (a['id']) in quiz_key.keys() :
        # don't deal with questions that have since been removed from quiz.
        
        
        results = [{
                    'question':         int(a['id']),
                    'actual':    int(a['answer']),
                    'correct':   answer_key[int(a['id'])],
                    'quiz_number':      quiz_key  [int(a['id'])]
        } for a in score if int (a['id']) in quiz_key.keys() ]
          
        quiz_scores = []
        
        ###
        #print the_student.username
        
        
        for quiz in quizzes:
            ###
            #print 'quiz_%d' % quiz.id
            try:
                raw_quiz_info = simplejson.loads (state.json)['quiz_%d' % quiz.id]
            except:
                raw_quiz_info = {}
            ###
            #print raw_quiz_info
            
            
                
            answer_count = len([a for  a in results if a['quiz_number'] == quiz.id ])
            
            
            if answer_count or raw_quiz_info.has_key ( 'all_correct' ) or raw_quiz_info.has_key ( 'initial_score'):
                #print "let's try it"       
                correct_count = len([a for  a in results if a['correct'] == a['actual'] and a['quiz_number'] == quiz.id ])
                quiz_results = { 'quiz': quiz, 'score': correct_count, 'answer_count' : answer_count}
                
                
                
                
                try:
                    if raw_quiz_info['all_correct']:
                        quiz_results ['all_correct'] =  raw_quiz_info['all_correct']
                except:
                    pass
                
                
                
                
                try:
                    if raw_quiz_info['initial_score']:
                        quiz_results ['initial_score'] =  raw_quiz_info['initial_score']
                except:
                    pass
               
                quiz_scores.append(quiz_results)
        
        #print "ok final result for this user is:"
        #print quiz_scores
        
        return quiz_scores

#SEE  http://www.columbia.edu/acis/rad/authmethods/auth-affil
# see http://www.columbia.edu/acis/rad/authmethods/wind/ar01s06.html
#    students = User.objects.all()

def score_info_for_class (course_info):
    cache_key = "score_info_for_t%s.y%s.s%s.c%s%s.%s" % course_info
    if cache.get(cache_key):
        return cache.get(cache_key)
    result = dict([(a, score_on_all_quizzes(a)) for a in students_in_class(course_info)])
    cache.set(cache_key,result,60*60)
    return result
                
def summarize_score_info_for_class (course_info):
    info = score_info_for_class (course_info)
    students_with_scores =  [v for v in info.values() if v]
    pre_test_count = 0
    post_test_count = 0
    
    for a in students_with_scores:
        for b in a:
            #print b['quiz'].label()
            if b['quiz'].label() == 'Pre-test':
                pre_test_count = pre_test_count + 1
            
            
            if b['quiz'].label() == 'Post-test':
                if b['all_correct'] == 't':
                    post_test_count = post_test_count + 1

    #print course_info
    #print  {'pre_test' : pre_test_count, 'post_test': post_test_count}
    return {'pre_test' : pre_test_count, 'post_test': post_test_count}

def question_and_quiz_keys():
    questions = Question.objects.all()
    quizzes = Quiz.objects.all()
    
    quiz_key = {}
    answer_key = {}
    
    for question in questions:
        try:
            answer_key [question.id ] = question.answer_set.get(correct=True).id 
            quiz_key [question.id ] = question.quiz.id
        except:
            pass

    return { 'answer_key':answer_key, 'quiz_key':quiz_key}


@rendered_with('quiz/scores_student.html')
def scores_student(request):
    return {
        'scores':  score_on_all_quizzes (request.user),
        'score_on_bruise_recon' : score_on_bruise_recon(request.user),
        'score_on_taking_action' : score_on_taking_action(request.user),
        'site' : Site.objects.get_current()
    }
    

@rendered_with('quiz/scores_faculty_courses.html')
def scores_faculty_courses(request):
    if request.user.user_type() == 'student':
        return scores_student(request)
    return {
        'site' : Site.objects.get_current()
    }

#show results for all students in one course.
@rendered_with('quiz/scores_faculty_course.html')
def scores_faculty_course(request, c1, c2, c3, c4, c5, c6):
    
    
    if request.user.user_type() == 'student':
        return scores_student(request)
    
    course_info = (c1, c2, c3, c4, c5, c6)
    course_string = "t%s.y%s.s%s.c%s%s.%s.st" % course_info
    

    students_to_show = students_in_class(course_info)


    questions = Question.objects.all()
    quizzes = Quiz.objects.all()
    
    result = []

    tmp = question_and_quiz_keys()
    answer_key = tmp ['answer_key']
    quiz_key =   tmp ['quiz_key']
    
    #pdb.set_trace()
    for student in students_to_show:
        try:
            result.append (
                {
                    'student': student,
                    'scores':  score_on_all_quizzes (student),
                    'score_on_bruise_recon' : score_on_bruise_recon(student),
                    'score_on_taking_action' : score_on_taking_action(student)
                }
            )
        except:
             result.append (
                {
                    'student': student,
                    'scores':  None,
                    'score_on_bruise_recon' : None,
                    'score_on_taking_action' : None
                }
            )
    
    
    return { 'c' : course_info , 'student_info' : result,  'site' : Site.objects.get_current()}


@rendered_with('quiz/scores_admin.html')
def scores_admin(request):
    """
    Show ALL THE SCORES, for ALL THE STUDENTS. EVER.
    
    Note: this is much more efficient than it might look at first glance,
    and plenty efficient for the first couple semesters.
    We can also come back and optimize it further once we have actual data.
   
    Faculty members are also given student wind affils for the classes they teach.
    Therefore,  the trick is not to show classes unless there is
    *at least* one student who is not also faculty.
    
    Also, if we wanted to, we could further narrow classed down for the following school codes:
        pedi
        pros
        regi
        opdn
        socw    
    """

    if request.user.user_type() == 'student':
        return scores_student(request)

    all_affils = Group.objects.all()
    tmp = [re.match('t(\d).y(\d{4}).s(\d{3}).c(\w)(\d{4}).(\w{4}).(\w{2})',c.name) for c in all_affils]
    course_matches = [a for a in tmp if a != None]
    relevant_classes = []
    launch_year = 2010
    results = [  ]
    checked = [  ]
    term_key = {
        '1': 'Spring ',
        '2': 'Summer ',
        '3': 'Fall ',
        '4': 'Winter '
    }
    
    for course_info in [a.groups()[0:6]  for a in course_matches]:
        f_lookup = "t%s.y%s.s%s.c%s%s.%s.fc"
        s_lookup = "t%s.y%s.s%s.c%s%s.%s.st"
        if course_info not in checked:            
            checked.append (course_info)
            if int(course_info[1]) >= launch_year:
                faculty_affils_list = [a for a in all_affils if f_lookup % course_info in a.name]
                student_affils_list = [a for a in all_affils if s_lookup % course_info in a.name]
                if faculty_affils_list and student_affils_list:
                    faculty =  faculty_affils_list[0].user_set.all()
                    students = student_affils_list[0].user_set.all()
                    if [s for s in students if s not in faculty]:
                        #pdb.set_trace()
                        results.append ( {
                             'course_string': "%s %s%s, section %s" % \
                             (course_info[5], course_info[3], course_info[4],course_info[2]),
                             'faculty' : faculty,
                             'semester' : term_key[course_info[0]] + course_info[1],
                             'course_info' : course_info,
                             'score_info_for_class' : summarize_score_info_for_class (course_info),
                             'number_of_students_in_class' : number_of_students_in_class (course_info),
                        })
                else:
                    pass
            else:
                pass
        else:
            pass
            
    return {    
        'courses' : results,
        'site' : Site.objects.get_current()
    }

@rendered_with('quiz/studentquiz.html')
def studentquiz(request, quiz_id, user_id):
    """allows a faculty member to see the answers a student posted for a quiz.
    URL, btw, is: /activity/quiz/studentquiz/2/user/5/ """    
    if request.user.user_type() == 'student':
        return scores_student(request)

    student = get_object_or_404(User,id=user_id)
    quiz = get_object_or_404(Quiz,id=quiz_id)
    
    return {
        'student' : student,
        'quiz'  : quiz,
        'student_json': state_json (student)
    }

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


@rendered_with('quiz/edit_answer.html')
def edit_answer(request,id):
    answer = get_object_or_404(Answer,id=id)
    return dict(answer=answer)

def state_json (user):
    try: 
        state = ActivityState.objects.get(user=user)
        if (len(state.json) > 0):
            doc = state.json
    except ActivityState.DoesNotExist:
        doc = "{}"
    return doc

@login_required
def loadstate(request):
    response = HttpResponse(state_json(request.user), 'application/json')
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
