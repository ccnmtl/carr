from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from pagetree.models import Hierarchy
from django.contrib.auth.decorators import login_required
from carr_main.models import SiteState, user_sort_key, sort_users, user_type
from django.contrib.sites.models import Site, RequestSite
from quiz.models import Quiz, Question, Answer
from activity_taking_action.models import score_on_taking_action
from activity_bruise_recon.models import score_on_bruise_recon
from quiz.scores import score_on_all_quizzes, all_answers_for_quizzes, scores_student, training_is_complete
from django.contrib.sites.models import Site, RequestSite
from django.conf import settings
import re

#import datetime


def background(request,  content_to_show):
    if content_to_show not in ['credits', 'contact', 'about']:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    file_name = {
        'about' : 'about.html',
        'credits' : 'credits.html',
        'contact' : 'contact.html',
    } [content_to_show]
    t = loader.get_template('carr_main/background/%s' % file_name)
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))    
    


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




@login_required
@rendered_with('carr_main/page.html')
def page(request,path):
    h = Hierarchy.get_hierarchy('main')
    current_root = h.get_section_from_path(path)    
    section = h.get_first_leaf(current_root)
    ancestors = section.get_ancestors()
    ss = SiteState.objects.get_or_create(user=request.user)[0]
    current_site = Site.objects.get_current()
    
    
    
    # Skip to the first leaf, make sure to mark these sections as visited
    if (current_root != section):
        ss.set_has_visited(ancestors)
        return HttpResponseRedirect(section.get_absolute_url())
    
    # the previous node is the last leaf, if one exists.
    prev = section.get_previous_site_section()
    next = section.get_next_site_section()  
    
    # Is this section unlocked now?
    can_access = _unlocked(section, request.user, prev, ss)
    if can_access:
        #just to avoid drama, only save last location if the section is available on both sites.
        #import pdb
        #pdb.set_trace()
        ss.save_last_location(request.path, section)
        
    module = None
    if not section.is_root:
        module = ancestors[1]
        
    # construct the subnav up here. it's too heavy on the client side
    subnav = _construct_menu(request, module, section, ss)
        
    # construct the left nav up here too.
    depth = section.depth()
    parent = section
    if depth == 3:
        parent = section.get_parent()
    elif depth == 4:
        parent = section.get_parent().get_parent()
    elif depth == 5:
        parent = section.get_parent().get_parent().get_parent()
        
    leftnav = _construct_menu(request, parent, section, ss)
    
    
    #ok let's try this
    ss.set_has_visited([section])
    
    return dict(section=section,
                accessible=can_access,
                module=module,
                root=ancestors[0],
                previous=prev,
                next=next,
                subnav=subnav,
                depth=depth,
                site_domain=current_site.domain,
                leftnav=leftnav)

def wind_affil (section_key_dict):
    d = section_key_dict
    vals = (
            d['term_number']
        ,   d['year']
        ,   d['section']
        ,   d['term_character']
        ,   d['course_string']
        ,   d['department']
    )
    prefix = 't%s.y%s.s%s.c%s%s.%s' % vals
    return (
        ( '%s.st.course:columbia.edu' % prefix ).lower(),
        ( '%s.fc.course:columbia.edu' % prefix ).lower()
    ) 

def extract_section_keys (the_string):
    keys =  ['year', 'term_number', 'department', 'course_string', 'term_character', 'section']
    components = [
        '\d\d\d\d'    # year
        ,  '\d'       # term number
        ,  '[A-Z]{4}' # department
        ,  '\d\d\d.'  # course_string
        ,  '[A-Z]'    # term_character
        ,  '\d\d\d'   # section
    ]
    what_to_match = ''.join ( '(' + c + ')' for c in components)
    matches = re.findall(what_to_match, the_string)
    result =  [ wind_affil(dict( zip (keys, m))) for m in matches] 
    return result

#just for testing:
if 1 == 0:
    def get_dummy_user ():
         return User.objects.get(username='egr2107')

def add_course (stg, fcg):
    """ Look up the student and faculty WIND affils for a course.
    If they don't exist, create them.
    Add the default social work school faculty to the affils."""
    
    default_faculty = User.objects.filter (id__in= settings.DEFAULT_SOCIALWORK_FACULTY_USER_IDS)
    already_existing_student_affils = Group.objects.filter(name__icontains=stg)
    already_existing_faculty_affils = Group.objects.filter(name__icontains=fcg)
    
    
    #####################
    ##### FACULTY AFFILS:
    if not already_existing_faculty_affils:
        new_faculty_affil = Group (name = fcg)
        new_faculty_affil.save()
    else:
        #Faculty affil already exists.
        new_faculty_affil = already_existing_faculty_affils[0]    

    #####################
    ##### STUDENT AFFILS:
    if not already_existing_student_affils:
        new_student_affil = Group (name = stg)
        new_student_affil.save()
    else:
        #Student affil already exists.
        new_student_affil = already_existing_student_affils[0]    



    #add a student: (just for testing)
    if 1 == 0:
        dummy_user = get_dummy_user ()
        dummy_user.groups.add(new_student_affil)
        dummy_user.save()


    #####################
    for instructor in default_faculty:
        new_student_affil.user_set.add(instructor)
        new_student_affil.save()
        new_faculty_affil.user_set.add(instructor)
        new_faculty_affil.save()
        instructor.save()


@login_required
@rendered_with('carr_main/add_classes/add_classes_form.html')
def add_classes(request):
    default_faculty = User.objects.filter (id__in= settings.DEFAULT_SOCIALWORK_FACULTY_USER_IDS)
    sorted_default_faculty =  sorted ( default_faculty, key=lambda x: x.last_name)
    section_keys = ''
    found_section_keys = {}
    if not request.POST:
        return  {
            'section_keys': 'Enter course section keys here!'
            ,'default_faculty': sorted_default_faculty
        }
    if not request.POST.has_key ('section_keys'):
        return  { 
            'default_faculty': sorted_default_faculty
            ,'error': 'No courses found.'
        }
    if request.POST['section_keys'] == '':
        return  { 
            'default_faculty': sorted_default_faculty  
            ,'error': 'No courses found.'
        }
    section_keys = request.POST['section_keys']
    found_section_keys =  extract_section_keys (section_keys)
    if len (found_section_keys) ==  0:
        return  { 
            'default_faculty': sorted_default_faculty
            ,'error': 'No courses found.'
        }
    #ok we now have actual courses.
    for stg, fcg in found_section_keys:
        add_course (stg, fcg)

    return {
        'default_faculty': sorted_default_faculty
        ,'section_keys' : section_keys
        ,'success' : True
        ,'found_section_keys' : found_section_keys
    }


@login_required
@rendered_with('carr_main/selenium.html')
def selenium(request,task):
    if task =='setup':
        test_user = User.objects.get(username = 'student1')
        [a.delete() for a in test_user.bruise_recon_user.all()]
        [a.delete() for a in test_user.taking_action_user.all()]
        [a.delete() for a in test_user.quiz_user.all()]
            
        try:    
            SiteState.objects.get(user=test_user).delete()
        except SiteState.DoesNotExist:
            pass
            
        sel_message = "proceed"
   
    if task =='teardown':
        pass
    
    return dict(task=task, sel_message=sel_message)    
    
    
if 1 == 3:    
    def to_python_date (timestring):
        try:
            return datetime.datetime.strptime (' '.join (timestring.split(' ')[0:5]), "%a %b %d %Y %H:%M:%S")
        except ValueError:
            #sometimes JS doesn't give us the year,  which results in the date being 1900... not good but better than a 500 error...
            return datetime.datetime.strptime (' '.join (timestring.split(' ')[0:4]), "%a %b %d %H:%M:%S")    



@login_required
@rendered_with('carr_main/stats.html')
def stats(request,task):
    """ 
    THIS IS IN BETA.

    Two tables with one row per student. This will get very large/slow and is only really intended to be run infrequently. We will cache it once a day or two once it stabilizes..

    TODO: add date information for quizzes
    TODO: allow to specify semester / school via request
    TODO: show initial answers for students who have them.
    """
    
    if request.user.user_type() == 'student':
        return scores_student(request)
    
    #TODO: narrow down users based on task
    if task =='registrar_summary':
        pass
        
    if task =='question_comparison':
        pass
    
    #for now just use all users.
    #tmp = [ u for u in User.objects.all() if 'aa' in u.username]
    tmp = [ u for u in User.objects.all() ]
    
    the_users = sort_users([ u for u in tmp if u.user_type() == 'student'  ]) 
    
    pre_test_questions  = Question.objects.filter(quiz__id = 2)
    post_test_questions = Question.objects.filter(quiz__id = 3)
    
    case_1_questions =    Question.objects.filter(quiz__id = 6)
    case_2_questions =    Question.objects.filter(quiz__id = 7)
    case_3_questions =    Question.objects.filter(quiz__id = 8)
    
    blarg = []
    blarg.extend(pre_test_questions)
    blarg.extend(case_1_questions)
    blarg.extend(case_2_questions)
    blarg.extend(case_3_questions)
    blarg.extend(post_test_questions)
    
    questions_in_order = [(str(q.id), q ) for q in blarg ]
    
    site          = Site.objects.get_current (  )

    the_stats = {}
    for u in the_users:
    
        _quizzes       = score_on_all_quizzes     (u)
        _bruise_recon  = score_on_bruise_recon    (u)
        _taking_action = score_on_taking_action   (u)
        
        student_training_is_complete = training_is_complete (u, _quizzes, _bruise_recon, _taking_action, site)
        
        #print student_training_is_complete
        the_stats[u.username] = {}
        the_stats[u.username]['user_object'] = u
        the_stats[u.username]['completed_training'] = student_training_is_complete
        the_stats[u.username]['taking_action'] = _taking_action
        the_stats[u.username]['bruise_recon'] = _bruise_recon
        student_score_on_all_quizzes = _quizzes
        the_stats[u.username]['quizzes'] = student_score_on_all_quizzes
        
        #get completion times (refactor)?
        try:
            tmp = [(z['submit_time']) for z in student_score_on_all_quizzes if  z.has_key ('quiz') and z.has_key ('submit_time') and  z['quiz'].id == 3]
            if len (tmp) > 0:
                all_submit_times_for_post_test = tmp [0]
                if len(all_submit_times_for_post_test) > 0:
                    the_stats[u.username]['completion_time'] = all_submit_times_for_post_test[-1]
                else:
                    the_stats[u.username]['completion_time'] = "no completion time found (length zero 1)" # this shouldn't occur.
            else:
                the_stats[u.username]['completion_time'] =  "(no time recorded)"
        except  KeyError:
             the_stats[u.username]['completion_time'] = "no completion time found (key error)" #this shouldn't occur.
        
                
        all_answers = all_answers_for_quizzes(u)
        the_stats[u.username]['answers_in_order'] = []
        for question_id_string, question in questions_in_order:
            found = False
            for question_id, correct_incorrect in all_answers.iteritems():
                if question_id_string == str(question_id):
                    the_stats[u.username]['answers_in_order'].append(correct_incorrect)
                    found = True
            if not found:
                the_stats[u.username]['answers_in_order'].append("")
            
    return dict(task = task,
                stats = the_stats,
                users = the_users, 
                questions_in_order = questions_in_order,
                site = Site.objects.get_current())    
    

@login_required
def index(request):
    print "index"
    try:
        ss = SiteState.objects.get(user=request.user)
        url = ss.last_location
        if url == '':
            url = '/carr'
    except SiteState.DoesNotExist:
        url = "/carr"
    
    return HttpResponseRedirect(url)


#####################################################################
## View Utility Methods
    
def _construct_menu(request, parent, section, ss):
    menu = []
    current_site = Site.objects.get_current()
    siblings = [ a for a in parent.get_children() if current_site in a.sites()]
    
    for s in siblings:
        entry = {'section': s, 'selected': False, 'descended': False, 'accessible': False}
        if s.id == section.id:
            entry['selected'] = True
        
        if section in s.get_descendents():
            entry['descended'] = True
            
        previous = s.get_previous_leaf()
            
        if _unlocked(s, request.user, previous, ss):
            entry['accessible'] = True
            
        menu.append(entry)
        
    return menu

def _unlocked(section,user,previous,sitestate):
    """ if the user can proceed past this section """
    #import pdb
    #pdb.set_trace()
    
    
    if not section or section.is_root or sitestate.get_has_visited(section):
       return True
    
    
    if not previous or previous.is_root:
        return True
    
    for p in previous.pageblock_set.all():
        if hasattr(p.block(),'unlocked'):
           if p.block().unlocked(user) == False:
              #print p
              #print p.block()
              #print p.block().unlocked(user)
              return False
    return sitestate.get_has_visited(previous)



