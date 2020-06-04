""" This is a series of views that in some ways belong in the Quiz
module, and in others don't. Maybe they need to be moved to their own
app. For now they definitely get their own module."""

import csv
import datetime
import json
import re

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pagetree.models import PageBlock

from carr.activity_bruise_recon.models import score_on_bruise_recon
from carr.activity_taking_action.models import score_on_taking_action
from carr.carr_main.models import students_in_class, users_by_uni, user_type
from carr.quiz.models import Answer, Quiz, Question, ActivityState
from carr.utils import get_students, filter_users_by_affiliation


def can_see_scores(u):
    return (u.is_authenticated and user_type(u) in ('faculty', 'admin'))


def year_range():
    next_year = datetime.datetime.now().year + 2
    return range(2010, next_year)


semester_map = {1: 'spring', 2: 'summer', 3: 'fall'}
inv_semester_map = dict((v, k) for k, v in semester_map.items())


@user_passes_test(can_see_scores)
def access_list(request):
    whitelist = settings.DEFAULT_SOCIALWORK_FACULTY_UNIS
    allowed = []
    for u in User.objects.all().order_by('last_name'):
        groups = [g.name for g in u.groups.all()]
        u.whitelist = u.username in whitelist
        u.admin = any([('tlcxml' in g) for g in groups])
        u.faculty = any([('.fc.' in g) for g in groups]) or u.is_staff
        if any([u.whitelist, u.admin, u.faculty]):
            allowed.append(u)
    return render(request, 'quiz/scores/access_list.html',
                  dict(allowed=allowed))


@user_passes_test(can_see_scores)
def scores_index(request):
    return render(request, 'quiz/scores/scores_index.html', {
        'full_page_results_block': True,
        'hide_scores_help_text': True,
    })


@user_passes_test(can_see_scores)
def socialwork_overview(request):
    return render(request, 'quiz/scores/socialwork_overview.html', {
        'years': year_range()
    })


@user_passes_test(can_see_scores)
def semesters_by_year(request, year):
    return render(request, 'quiz/scores/semesters_by_year.html', {
        'year': year, 'semester_map': semester_map
    })


def sort_courses(courses):
    return sorted(courses,
                  key=lambda c: (c['course_label'], c['course_section']))


def push_time(timelist):
    timelist.append(datetime.datetime.now())


@user_passes_test(can_see_scores)
def classes_by_semester(request, year, semester):
    if user_type(request.user) == 'student':
        return scores_student(request)
    semester_string = 't%s.y%s' % (inv_semester_map[semester], year)
    all_affils = Group.objects.all()
    this_semester_affils = [
        a for a in all_affils
        if semester_string in a.name and 'socw' in a.name]
    care_classes = find_care_classes(this_semester_affils)
    sorted_care_classes = sort_courses(care_classes)
    return render(request, 'quiz/scores/classes_by_semester.html', {
        'year': year, 'hide_scores_help_text': True, 'semester_map':
        semester_map, 'semester': semester, 'care_classes': sorted_care_classes
    })


@user_passes_test(can_see_scores)
def students_by_class(request, c1, c2, c3, c4, c5, c6):
    course_info = (c1, c2, c3, c4, c5, c6)
    students_to_show = students_in_class(course_info)
    return render(request, 'quiz/scores/students_by_class.html', {
        'c': course_info, 'semester':
        semester_map[int(course_info[0])], 'year': course_info[1],
        'student_info': get_student_info(students_to_show),
        'full_page_results_block': True
    })


@user_passes_test(can_see_scores)
def student_lookup_by_uni_form(request):
    template_name = 'quiz/scores/student_lookup_by_uni.html'
    rp = request.POST
    if 'uni' not in rp:
        # just a get request. return the empty form.
        return render(request, template_name, {
            'student': None, 'full_page_results_block':
            True, 'student': None
        })

    uni = rp['uni']
    if len(uni) < 3:
        return render(request, template_name, {
            'student': None,
            'full_page_results_block': True,
            'error':
            "Plase enter at least 3 letters from the student's UNI."
        })

    found_students = users_by_uni(uni)
    if len(found_students) == 0:
        return render(request, template_name, {
            'student': None, 'full_page_results_block':
            True, 'uni': uni,
            'error':
            ("The UNI you entered could not be found. "
             "Please check the UNI and try again.")
        })

    student_info = get_student_info(found_students)
    return render(request, template_name, {
        'full_page_results_block': True, 'uni': uni, 'student':
        'student', 'student_info': student_info, 'error': None
    })


@user_passes_test(lambda u: u.is_authenticated)
def scores_student(request):
    try:
        if user_type(request.user) == 'student':
            pass
    except AttributeError:
        return HttpResponseRedirect('/')

    """ A summary of a the currently logged in user's results."""
    ru = request.user
    quizzes = score_on_all_quizzes(ru)
    bruise_recon = score_on_bruise_recon(ru)
    taking_action = score_on_taking_action(ru)
    site = get_current_site(request)

    return render(request, 'quiz/scores_student.html', {
        'scores': quizzes,
        'score_on_bruise_recon': bruise_recon,
        'score_on_taking_action': taking_action,
        'training_complete':
        training_is_complete(
            ru,
            quizzes,
            bruise_recon,
            taking_action,
            site),
        'site': site
    })


def to_python_date(timestring):
    try:
        return (
            datetime.datetime.strptime(
                ' '.join(timestring.split(' ')[0:5]),
                "%a %b %d %Y %H:%M:%S")
        )
    except ValueError:
        # sometimes JS doesn't give us the year,  which results in the date
        # being 1900... not good but better than a 500 error...
        return (
            datetime.datetime.strptime(
                ' '.join(timestring.split(' ')[0:4]),
                "%a %b %d %H:%M:%S")
        )


def get_student_info(students):
    site = Site.objects.get_current()
    result = []
    for student in students:
        quizzes = score_on_all_quizzes(student)
        bruise_recon = score_on_bruise_recon(student)
        taking_action = score_on_taking_action(student)
        result.append({
            'student': student,
            'scores': quizzes,
            'score_on_bruise_recon': bruise_recon,
            'score_on_taking_action': taking_action,
            'training_complete': training_is_complete(
                student, quizzes, bruise_recon, taking_action, site)
        })
    return result

# a couple helper functions for scoring:


def get_quiz_score(quiz, json_stream, results):
    try:
        raw_quiz_info = json_stream['quiz_%d' % quiz.id]
    except (KeyError):
        raw_quiz_info = {}
    answer_count = len(
        [a for a in results if a['quiz_number'] == quiz.id])
    if not (answer_count or
            'all_correct' in raw_quiz_info or
            'initial_score' in raw_quiz_info):
        return None

    correct_count = len(
        [a for a in results
         if a['correct'] == a['actual'] and
         a['quiz_number'] == quiz.id])
    quiz_results = {
        'quiz': quiz,
        'score': correct_count,
        'answer_count': answer_count}
    if 'all_correct' in raw_quiz_info:
        quiz_results[
            'all_correct'] = raw_quiz_info['all_correct']
    if 'initial_score' in raw_quiz_info:
        quiz_results[
            'initial_score'] = raw_quiz_info['initial_score']
    # Add dates too:
    if 'submit_time' in raw_quiz_info:
        quiz_results['submit_time'] = [
            to_python_date(x)
            for x in raw_quiz_info['submit_time']]
    return quiz_results


def score_on_all_quizzes(the_student):
    tmp = question_and_quiz_keys()
    answer_key = tmp['answer_key']
    quiz_key = tmp['quiz_key']
    quizzes = tmp['quizzes']

    try:
        state = ActivityState.objects.get(user=the_student)
    except ActivityState.DoesNotExist:
        return []

    if len(state.json) == 0:
        return []

    score = []
    json_stream = json.loads(state.json)
    for a in json_stream.values():
        try:
            score.extend(a['question'])
        except KeyError:
            pass  # eh.

    # don't deal with questions that have since been removed from quiz.
    results = [{
        'question': int(a['id']),
        'actual': int(a['answer']),
        'correct': answer_key[int(a['id'])],
        'quiz_number': quiz_key[int(a['id'])]
    } for a in score if int(a['id']) in quiz_key.keys()]
    return get_quiz_scores(quizzes, json_stream, results)


def get_quiz_scores(quizzes, json_stream, results):
    quiz_scores = []
    for quiz in quizzes:
        r = get_quiz_score(quiz, json_stream, results)
        if r:
            quiz_scores.append(r)
    return quiz_scores


def load_state_json(the_student):
    try:
        state = ActivityState.objects.get(user=the_student)
    except ActivityState.DoesNotExist:
        return None

    if len(state.json) == 0:
        return None

    try:
        return json.loads(state.json)
    except ValueError:
        return None


def set_pre_test(json_stream, result):
    if json_stream['quiz_2']['initial_score']['quiz_score'] is not None:
        result['pre_test'] = True
    return result


def set_post_test(json_stream, result):
    if json_stream['quiz_3']['all_correct'] == 't':
        result['post_test'] = True
    return result


# a couple helper functions for scoring:
def pre_and_post_test_results(the_student):
    result = {'pre_test': False, 'post_test': False}

    json_stream = load_state_json(the_student)
    if json_stream is None:
        return result

    # initial test:
    try:
        result = set_pre_test(json_stream, result)
    except KeyError:
        return result

    # final test:
    try:
        result = set_post_test(json_stream, result)
    except KeyError:
        pass
    return result


def find_care_classes(affils):
    """If we can find users in our DB with ST affils for a course,
    AND users with FC affils, we consider that course a CARE course."""

    course_match_string = (r't(\d).y(\d{4}).s(\w{3}).c(\w)'
                           r'(\d{4}).(\w{4}).(\w{2})')
    tmp = [re.match(course_match_string, c.name) for c in affils]
    course_matches, results, checked = [x for x in tmp if x], [], []
    f_lookup = "t%s.y%s.s%s.c%s%s.%s.fc"
    s_lookup = "t%s.y%s.s%s.c%s%s.%s.st"

    for course_info in [a.groups()[0:6] for a in course_matches]:
        if course_info not in checked:
            checked.append(course_info)
            student_lookup_for_this_course = f_lookup % course_info
            faculty_lookup_for_this_course = s_lookup % course_info
            faculty_affils_list = [
                a for a in affils if student_lookup_for_this_course in a.name]
            if faculty_affils_list:
                student_affils_list = [
                    a for a in affils
                    if faculty_lookup_for_this_course in a.name]
                if faculty_affils_list and student_affils_list:
                    class_info = extract_class_info(
                        course_info,
                        faculty_affils_list,
                        student_affils_list)
                    if class_info is not None:
                        results.append(class_info)
        else:
            pass  # already checked this course.

    return results


def extract_class_info(course_info, faculty_affils_list, student_affils_list):
    """ Figure out what students and faculty are associated with this
    class based on WIND affils. If there are both students AND faculty
    associated with the class, we can assume it's a CARE class."""
    this_course_faculty = faculty_affils_list[0].user_set.all()
    students = student_affils_list[0].user_set.all()

    has_students = False
    has_default_faculty = False

    # check whether we at least have any students in this class:
    if len([s for s in students if s not in this_course_faculty]) > 0:
        # All the students are also faculty. This is probably a CARE course.
        has_students = True

    # Are the usual suspects teaching the class? If so let's display it even
    # if we don't know of any students yet.
    default_faculty = User.objects.filter(
        username__in=settings.DEFAULT_SOCIALWORK_FACULTY_UNIS)

    default_faculty_not_teaching_this_course = [
        f for f in default_faculty if f not in this_course_faculty]
    if len(default_faculty_not_teaching_this_course) == 0:
        has_default_faculty = True

    if not has_students and not has_default_faculty:
        return None

    the_students = [s for s in students if s not in this_course_faculty]

    return {
        'course_label':
        # TODO Sort by last name
        course_label(course_info),
        'course_section': course_section(course_info),
        'faculty': this_course_faculty,
        'course_info': course_info,
        'score_info_for_this_class': count_pretest_and_posttest_students(
            course_info, the_students),
        'number_of_students_in_class': len(the_students)
    }


def course_label(course_info):
    return "%s%s" % (course_info[3], course_info[4])


def course_section(course_info):
    return "%s" % (course_info[2])


def results_for_quiz_keys(quiz_keys_to_consider, answer_key):
    results = {}
    for a in quiz_keys_to_consider:
        question_id = int(a['id'])
        actual_answer_id = int(a['answer'])
        correct_answer_id = answer_key[int(a['id'])]
        results[question_id] = correct_token(actual_answer_id,
                                             correct_answer_id)
    return results


def all_answers_for_quizzes(the_student):
    """ For all the quizzes the student took, list whether the student
    answered correctly or not."""
    tmp = question_and_quiz_keys()
    answer_key = tmp['answer_key']
    quiz_key = tmp['quiz_key']
    try:
        state = ActivityState.objects.get(user=the_student)
    except ActivityState.DoesNotExist:
        return {}
    if (len(state.json) == 0):
        # TODO: this returns nothing. that's probably not right.
        return
    score = []
    for a in json.loads(state.json).values():
        try:
            score.extend(a['question'])
        except KeyError:
            pass

    quiz_keys_to_consider = [
        a for a in score if int(a['id']) in quiz_key.keys()]
    return results_for_quiz_keys(quiz_keys_to_consider, answer_key)


def correct_token(actual, correct):
    if actual == correct:
        return 'c'  # correct.
    else:
        return 'i'  # incorrect.


# SEE  http://www.columbia.edu/acis/rad/authmethods/auth-affil
# see http://www.columbia.edu/acis/rad/authmethods/wind/ar01s06.html
#    students = User.objects.all()
def score_info_for_class(course_info):
    """Quick cached version of the quiz results for this class
    NOTE: This may be obsolete.

    """
    cache_key = "score_info_for_t%s.y%s.s%s.c%s%s.%s" % course_info
    if cache.get(cache_key):
        return cache.get(cache_key)
    result = dict([(a, score_on_all_quizzes(a))
                  for a in students_in_class(course_info)])
    cache.set(cache_key, result, 60 * 60)
    return result


def count_pretest_and_posttest_students(course_info, the_students):
    """Count the number of students in this class who took the pretest
    and the post-test."""
    pre_test_count = 0
    post_test_count = 0
    for a in [pre_and_post_test_results(a) for a in the_students]:
        if a['pre_test']:
            pre_test_count = pre_test_count + 1
        if a['post_test']:
            post_test_count = post_test_count + 1
    return {'pre_test': pre_test_count, 'post_test': post_test_count}


def question_and_quiz_keys():
    quizzes = cache.get("quizzes")
    if not quizzes:
        quizzes = Quiz.objects.all()
        cache.set("quizzes", quizzes, 60 * 60)

    questions = cache.get("questions")
    if not questions:
        questions = Question.objects.all()
        cache.set("questions", questions, 60 * 60)

    quiz_key = cache.get("quiz_key")
    answer_key = cache.get("answer_key")
    if not quiz_key or not answer_key:
        quiz_key = {}
        answer_key = {}

        for question in questions:
            try:
                answer_key[question.id] = \
                    question.answer_set.get(correct=True).id
                quiz_key[question.id] = question.quiz.id
            except (KeyError, Answer.DoesNotExist):
                pass

        cache.set("quiz_key", quiz_key, 60 * 60)
        cache.set("answer_key", answer_key, 60 * 60)

    return (
        {'answer_key': answer_key,
         'quiz_key': quiz_key,
         'quizzes': quizzes,
         'questions': questions}
    )


def grandfather(quiz_data, user):
    """Due to shifting course requirements, certain students are
    considered to have completed the training even though they have
    not completed all the now-required activities. This method applies
    those rules and decides whether a student is "grandfathered" in
    under the old rules; in that case it returns true.
    """
    result = False
    try:
        quiz_date = quiz_data[2]
    except IndexError:
        return True  # no date -- this is an old user.

    if quiz_date.year == 1900:
        # This is because the front end javascript reported no year.
        if user.id < 880:
            result = True
        else:
            result = False
    else:
        if quiz_date < datetime.datetime(2011, 10, 10, 0, 0, 0):
            # So they're done."
            result = True
    return result


def quiz_dict(q):
    if 'submit_time' in q:
        return q['all_correct'], q['score'], max(q['submit_time'])
    if 'all_correct' in q:
        return q['all_correct'], q['score']
    return 'f', q['score']


def has_dental_affiliation(user):
    ''' Pull out the list of schools the user is affiliated with
    t1.y2004.s001.ct6009.socw.st.course:columbia.edu
    0term, 1year, 2section, 3term character, 4school, 5department'''
    for g in user.groups.all():
        pieces = g.name.split('.')
        if len(pieces) > 4 and pieces[4] == 'intc':
            return True

    return False


def unfinished_activities(user, scores):
    return any([c not in scores.keys()
                for c in ['Case 1', 'Case 2', 'Case 3']])


def training_is_complete(user, quizzes, bruise_recon, taking_action, site):
    """
    Is this student done with the training?  This is just a helper
    function as we're changing the rules for determining when a
    student is done with the training.  Initially, the rule was that
    the student was done with the training as soon the post-test was
    completed with with all correct answers.  Now we're changing this
    to say that students have to finish all the other activities as
    well.
    """
    scores = dict((q['quiz'].label(), quiz_dict(q)) for q in quizzes)

    # Rule 1: Everyone has to take the post-test in order to pass the course.
    if 'Post-test' not in scores:
        return False

    if scores['Post-test'][0] != 't':
        # Failed the post test
        return False

    # do they qualify for a "grandfather" exception? If so, we consider the
    # training complete.
    if grandfather(scores['Post-test'], user):
        return True

    # Rule 2: Successfully passed the post test, but not eligible for
    # grandfathering.  We need to check if they did all the other
    # activities too in order to determine whether they're done.
    if 'Pre-test' not in scores.keys() or bruise_recon is None:
        return False
    if not has_dental_affiliation(user) and unfinished_activities(
            user, scores):
        return False

    if taking_action == 'no_data' or bruise_recon is None:
        return False

    # OK they're done with the training.
    return True


class PostTestAnalysisView(View):

    def dispatch(self, *args, **kwargs):
        if not can_see_scores(self.request.user):
            return HttpResponseForbidden('forbidden')
        return super(PostTestAnalysisView, self).dispatch(*args, **kwargs)

    def get_social_work_students(self):
        return filter_users_by_affiliation('ssw', get_students())

    def get_posttest(self):
        return PageBlock.objects.get(label='Post-test').block()

    def correct_answer_id(self, question):
        return str(question.answer_set.filter(correct=True).first().id)

    def initialize(self, quiz):
        results = {}
        for q in quiz.question_set.all().prefetch_related('answer_set'):
            results[str(q.id)] = {
                'id': q.id,
                'text': q.text,
                'responses': 0,
                'correct': 0,
                'answer': self.correct_answer_id(q)}
        return results

    def analyze(self, posttest, results):
        key = 'quiz_{}'.format(posttest.id)
        states = ActivityState.objects.filter(
            user__in=self.get_social_work_students())

        for state in states:
            if not state or len(state.json) == 0:
                continue

            strm = json.loads(state.json)
            if (key not in strm or
                'initial_score' not in strm[key] or
                    'answers_given' not in strm[key]['initial_score']):
                continue

            for a in strm[key]['initial_score']['answers_given']:
                qid = a['id']
                results[qid]['responses'] += 1
                if a['answer'] == results[qid]['answer']:
                    results[qid]['correct'] += 1

        return results

    def post(self, request):
        quiz = self.get_posttest()

        results = self.initialize(quiz)
        results = self.analyze(quiz, results)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename=posttest_analysis.csv'
        writer = csv.writer(response)

        writer.writerow(['q', 'text', '% initial correct'])

        for key in sorted(results.keys()):
            value = results[key]
            writer.writerow([
                'q{}'.format(value['id']), value['text'],
                value['correct'] / float(value['responses']) * 100
            ])

        return response
