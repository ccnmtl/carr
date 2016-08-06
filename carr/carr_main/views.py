import datetime
import re

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.template import RequestContext, Context, loader
from pagetree.helpers import get_hierarchy, get_section_from_path, get_module
from pagetree.models import Hierarchy

from carr.activity_bruise_recon.models import score_on_bruise_recon
from carr.activity_taking_action.models import score_on_taking_action
from carr.quiz.models import Question
from carr.quiz.scores import score_on_all_quizzes, all_answers_for_quizzes, \
    training_is_complete, can_see_scores, scores_student
from carr.utils import filter_users_by_affiliation, get_students

from .models import (
    SiteState, user_type, get_previous_site_section,
    get_next_site_section)


def context_processor(request):
    return dict(MEDIA_URL=settings.MEDIA_URL)


@user_passes_test(can_see_scores)
def edit_page(request, path):
    section = get_section_from_path(path)
    h = get_hierarchy()
    return render(request, 'carr_main/edit_page.html',
                  dict(section=section,
                       module=get_module(section),
                       root=h.get_root()))


def background(request, content_to_show):
    if content_to_show not in ['credits', 'contact', 'about']:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    file_name = {
        'about': 'about.html',
        'credits': 'credits.html',
        'contact': 'contact.html',
    }[content_to_show]
    t = loader.get_template('carr_main/background/%s' % file_name)
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


@login_required
def page(request, path):
    h = Hierarchy.get_hierarchy('main')
    current_root = h.get_section_from_path(path)
    section = h.get_first_leaf(current_root)
    ancestors = section.get_ancestors()
    ss = SiteState.objects.get_or_create(user=request.user)[0]
    current_site = get_current_site(request)

    # Skip to the first leaf, make sure to mark these sections as visited
    if (current_root != section):
        ss.set_has_visited(ancestors)
        return HttpResponseRedirect(section.get_absolute_url())

    # the previous node is the last leaf, if one exists.
    prev = get_previous_site_section(section)
    next = get_next_site_section(section)

    # Is this section unlocked now?
    can_access = _unlocked(section, request.user, prev, ss)
    if can_access:
        # just to avoid drama, only save last location if the section
        # is available on both sites.  import pdb pdb.set_trace()
        ss.save_last_location(request.path, section)

    module = None
    if not section.is_root:
        module = ancestors[1]

    # construct the subnav up here. it's too heavy on the client side
    subnav = _construct_menu(current_site, request.user, module, section, ss)

    # construct the left nav up here too.
    depth = section.depth()
    parent = section
    if depth == 3:
        parent = section.get_parent()
    elif depth == 4:
        parent = section.get_parent().get_parent()
    elif depth == 5:
        parent = section.get_parent().get_parent().get_parent()

    leftnav = _construct_menu(current_site, request.user, parent, section, ss)

    # ok let's try this
    ss.set_has_visited([section])

    return render(request, 'carr_main/page.html',
                  dict(section=section,
                       accessible=can_access,
                       module=module,
                       root=ancestors[0],
                       previous=prev,
                       next=next,
                       subnav=subnav,
                       depth=depth,
                       site_domain=current_site.domain,
                       leftnav=leftnav))


def wind_affil(section_key_dict):
    d = section_key_dict
    vals = (
        d['term_number'], d['year'], d['section'], d[
            'term_character'], d['course_string'], d['department']
    )
    prefix = 't%s.y%s.s%s.c%s%s.%s' % vals
    return (
        ('%s.st.course:columbia.edu' % prefix).lower(),
        ('%s.fc.course:columbia.edu' % prefix).lower()
    )


def extract_section_keys(the_string):
    """
     Note: this function doesn't currently validate the section keys.
           If at least one of them is valid, this function extracts
           it won't complain if the others are malformed.
    """
    keys = ['year',
            'term_number',
            'department',
            'course_string',
            'term_character',
            'section']
    components = [
        '\d\d\d\d',    # year
        '\d',       # term number
        '[A-Z]{4}',  # department
        '\d\d\d.',  # course_string
        '[A-Z]',    # term_character
        '\w\w\w',   # section
    ]
    what_to_match = ''.join('(' + c + ')' for c in components)
    matches = re.findall(what_to_match, the_string)
    result = [wind_affil(dict(zip(keys, m))) for m in matches]
    return result


def add_course(stg, fcg):
    """ Look up the student and faculty WIND affils for a course.
    If they don't exist, create them.
    Add the default social work school faculty to the affils."""

    default_faculty = User.objects.filter(
        username__in=settings.DEFAULT_SOCIALWORK_FACULTY_UNIS)
    already_existing_student_affils = Group.objects.filter(name__icontains=stg)
    already_existing_faculty_affils = Group.objects.filter(name__icontains=fcg)

    #####################
    # FACULTY AFFILS:
    if not already_existing_faculty_affils:
        new_faculty_affil = Group(name=fcg)
        new_faculty_affil.save()
    else:
        # Faculty affil already exists.
        new_faculty_affil = already_existing_faculty_affils[0]

    #####################
    # STUDENT AFFILS:
    if not already_existing_student_affils:
        new_student_affil = Group(name=stg)
        new_student_affil.save()
    else:
        # Student affil already exists.
        new_student_affil = already_existing_student_affils[0]

    #####################
    for instructor in default_faculty:
        new_student_affil.user_set.add(instructor)
        new_student_affil.save()
        new_faculty_affil.user_set.add(instructor)
        new_faculty_affil.save()
        instructor.save()


@login_required
def add_classes(request):
    template_name = 'carr_main/add_classes/add_classes_form.html'
    default_faculty = User.objects.filter(
        username__in=settings.DEFAULT_SOCIALWORK_FACULTY_UNIS)
    sorted_default_faculty = sorted(
        default_faculty,
        key=lambda x: x.last_name)

    if not request.POST:
        return render(request, template_name, {
            'section_keys':
            'Enter course section key(s) here. Sample: 20121SOCW7114T005',
            'default_faculty': sorted_default_faculty
        })
    if 'section_keys' not in request.POST:
        return render(request, template_name, {
            'default_faculty': sorted_default_faculty,
            'error': 'No courses found.'
        })
    if request.POST['section_keys'] == '':
        return render(request, template_name, {
            'default_faculty': sorted_default_faculty,
            'error': 'No courses found.'
        })
    section_keys = request.POST['section_keys']
    found_section_keys = extract_section_keys(section_keys)
    if len(found_section_keys) == 0:
        return render(request, template_name, {
            'default_faculty': sorted_default_faculty,
            'error': 'No courses found.'
        })
    # ok we now have actual courses.
    for stg, fcg in found_section_keys:
        add_course(stg, fcg)

    return render(request, template_name, {
        'default_faculty': sorted_default_faculty,
        'section_keys': section_keys, 'success':
        True, 'found_section_keys': found_section_keys
    })


@login_required
def selenium(request, task):
    if task == 'setup':
        test_user = User.objects.get(username='student1')
        [a.delete() for a in test_user.bruise_recon_user.all()]
        [a.delete() for a in test_user.taking_action_user.all()]
        [a.delete() for a in test_user.quiz_user.all()]

        try:
            SiteState.objects.get(user=test_user).delete()
        except SiteState.DoesNotExist:
            pass

        sel_message = "proceed"

    if task == 'teardown':
        pass

    return render(request, 'carr_main/selenium.html',
                  dict(task=task, sel_message=sel_message))


@user_passes_test(can_see_scores)
def stats(request, task):
    """
    Two tables with one row per student. This will get very large/slow
    and is only really intended to be run infrequently. We will cache
    it once a day or two once it stabilizes..

    """
    if task not in ['ssw', 'dental']:
        return HttpResponseNotFound()

    stats_csv_filename = ('care_stats_%s.csv' %
                          datetime.datetime.now().isoformat()[:10])
    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename=%s' % stats_csv_filename

    t = loader.get_template('carr_main/stats_csv.html')

    if user_type(request.user) == 'student':
        return scores_student(request)

    the_users = get_students()

    # make a list of questions:
    pre_test_questions = Question.objects.filter(quiz__id=2)
    post_test_questions = Question.objects.filter(quiz__id=3)

    case_1_questions = Question.objects.filter(quiz__id=6)
    case_2_questions = Question.objects.filter(quiz__id=7)
    case_3_questions = Question.objects.filter(quiz__id=8)

    tmp2 = []
    tmp2.extend(pre_test_questions)
    tmp2.extend(case_1_questions)
    tmp2.extend(case_2_questions)
    tmp2.extend(case_3_questions)
    tmp2.extend(post_test_questions)

    questions_in_order = [(str(q.id), q) for q in tmp2]

    site = get_current_site(request)

    the_stats = generate_user_stats(the_users, site, task, questions_in_order)
    result = dict(task=task,
                  stats=the_stats,
                  users=the_users,
                  questions_in_order=questions_in_order,
                  site=site)

    c = Context(result)
    response.write(t.render(c))
    return response


def generate_user_stats(the_users, site, affiliation, questions_in_order):
    the_stats = {}

    site_users = filter_users_by_affiliation(affiliation, the_users)

    for u in site_users:
        _quizzes = score_on_all_quizzes(u)
        _bruise_recon = score_on_bruise_recon(u)
        _taking_action = score_on_taking_action(u)

        student_training_is_complete = training_is_complete(
            u,
            _quizzes,
            _bruise_recon,
            _taking_action,
            site)

        the_stats[u.username] = {}
        the_stats[u.username]['user_object'] = u
        the_stats[u.username]['affiliation'] = affiliation
        the_stats[u.username][
            'completed_training'] = student_training_is_complete
        the_stats[u.username]['taking_action'] = _taking_action
        the_stats[u.username]['bruise_recon'] = _bruise_recon
        student_score_on_all_quizzes = _quizzes
        the_stats[u.username]['quizzes'] = student_score_on_all_quizzes

        when_training_was_started = get_quiz_time(
            student_score_on_all_quizzes,
            2)
        the_stats[u.username]['pre_test_time'] = when_training_was_started

        when_training_was_completed = get_quiz_time(
            student_score_on_all_quizzes,
            3)
        the_stats[u.username]['completion_time'] = when_training_was_completed

        all_answers = all_answers_for_quizzes(u)
        the_stats[u.username]['answers_in_order'] = []
        for question_id_string, question in questions_in_order:
            found = False
            for question_id, correct_incorrect in all_answers.iteritems():
                if question_id_string == str(question_id):
                    the_stats[u.username]['answers_in_order'].append(
                        correct_incorrect)
                    found = True
            if not found:
                the_stats[u.username]['answers_in_order'].append("")
    return the_stats


def get_quiz_time(scores, quiz_id):
    tmp = [(z['submit_time'])
           for z in scores if 'quiz' in z and
           'submit_time' in z and
           z['quiz'].id == quiz_id]
    if len(tmp) > 0:
        all_submit_times = tmp[0]
        if len(all_submit_times) > 0:
            result = all_submit_times[-1]
        else:
            result = "no timestamp found"
    else:
        result = "no timestamp found"
    return result


@login_required
def index(request):
    try:
        ss = SiteState.objects.get(user=request.user)
        url = ss.last_location
        if url == '' or url == '/':
            url = '/carr'
    except SiteState.DoesNotExist:
        url = '/carr'

    return HttpResponseRedirect(url)


#####################################################################
# View Utility Methods

def _construct_menu(current_site, user, parent, section, ss):
    menu = []
    siblings = [a for a in parent.get_children() if current_site in a.sites()]

    for s in siblings:
        entry = {
            'section': s,
            'selected': False,
            'descended': False,
            'accessible': False}
        if s.id == section.id:
            entry['selected'] = True

        if section in s.get_descendents():
            entry['descended'] = True

        previous = s.get_previous_leaf()

        if _unlocked(s, user, previous, ss):
            entry['accessible'] = True

        menu.append(entry)

    return menu


def _unlocked(section, user, previous, sitestate):
    """ if the user can proceed past this section """

    if not section or section.is_root or sitestate.get_has_visited(section):
        return True

    if not previous or previous.is_root:
        return True

    for p in previous.pageblock_set.all():
        if hasattr(p.block(), 'unlocked'):
            if not p.block().unlocked(user):
                return False
    return sitestate.get_has_visited(previous)
