from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from pagetree.models import Hierarchy
from django.contrib.auth.decorators import login_required
from carr_main.models import SiteState, user_sort_key, sort_users, user_type
from django.contrib.sites.models import Site, RequestSite
from quiz.models import Quiz, Question, Answer
from activity_taking_action.models import score_on_taking_action
from activity_bruise_recon.models import score_on_bruise_recon
from quiz.views import score_on_all_quizzes, all_answers_for_quizzes

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


@login_required
@rendered_with('carr_main/selenium.html')
def selenium(request,task):
    if task =='setup':
        #import pdb
        #pdb.set_trace()
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
    
    
    

@login_required
@rendered_with('carr_main/stats.html')
def stats(request,task):
    """ 
Two tables with one row per student. This will get very large and is only really intended to be run infrequently. We will cache it once a day.

registrar_summary:

   1. Student first name
   2. student last name
   3. UNI
   4. Course number
   5. Section number
   6. Term and year
   7. date "completed" CARE

8.pre-test score including which questions the student answered incorrectly (we'll need to be able to identify which questions students consistently get wrong so we can look at the questions)
9. activity: abuse or accident - students response for each
10. case 1
11. case 2
12. case 3
13. Taking action (This one seems a bit more difficult) I'm not sure if any data is being saved for this activity. It looks like it is either complete or n/a.
14 Post-test initial score including which questions the student answered incorrectly (we'll need to be able to identify which questions students consistently get wrong so we can look at the questions) [We need to be able to match the 10 pre-test questions with their identical 10 post-test questions. Is this something we can build into the data structure?]


question_comparison:
  1. A breakdown of all the questions in the pre-test, along with whether or not the students answered the individual questions correctly or not.

  2. A breakdown of the individual cases in the Activity: Cases and whether or not the students answered the question for each case correctly or not.

  3. One column for the Activity: Taking Action and whether or not the students completed this.

  4. One column for the post-test initial score.

  5. One column for the Post-Test status.

  These can be individual spreadsheets. Ideally, each spreadsheet will be sortable so that we can tally % correct, incorrect, missing, etc.


http://kodos.ccnmtl.columbia.edu:64757/stats/registrar_summary/

and

http://kodos.ccnmtl.columbia.edu:64757/stats/question_comparison/
"""


    # from carr_main.models import SiteState, user_sort_key, sort_users, user_type
    #import pdb
    #pdb.set_trace()
    #for now, just do all users with unis starting  with A:
    #the_users = sort_users([ u for u in User.objects.all() if u.username < 'b' and u.user_type() == 'student'])
    #all_questions = Question.objects.all()
    
    the_users = sort_users([ u for u in User.objects.all() if u.user_type() == 'student' ]) 
    
    #and u.username in [ 'amr2223', 'aab2175', 'ao2365']
    
    #blarg =  Question.objects.all().filter(quiz__id = 3)
    #import pdb
    #pdb.set_trace()
    
    pre_test_questions  = Question.objects.all().filter(quiz__id = 2)
    post_test_questions = Question.objects.all().filter(quiz__id = 3)
    
    case_1_questions =    Question.objects.all().filter(quiz__id = 6)
    case_2_questions =    Question.objects.all().filter(quiz__id = 7)
    case_3_questions =    Question.objects.all().filter(quiz__id = 8)
    
    blarg = []
    blarg.extend(pre_test_questions)
    blarg.extend(case_1_questions)
    blarg.extend(case_2_questions)
    blarg.extend(case_3_questions)
    blarg.extend(post_test_questions)
    
    tmp = Question.objects.all().order_by("quiz")
    questions_in_order = [(str(q.id), q ) for q in blarg ]
    
    
    #print questions_in_order
    
    #import pdb
    #pdb.set_trace()
    
    the_stats = {}
    for u in the_users:
    
        print u.username
        
        the_stats[u.username] = {}
        
        the_stats[u.username]['user_object'] = u
        the_stats[u.username]['taking_action'] = score_on_taking_action(u)
        the_stats[u.username]['bruise_recon'] = score_on_bruise_recon(u)
        the_stats[u.username]['quizzes'] = score_on_all_quizzes(u)
        the_stats[u.username]['answers'] = {}
        
        for question_id, correct_incorrect in all_answers_for_quizzes(u).iteritems():
            the_question = Question.objects.get(pk=question_id)
            the_stats[u.username]['answers'] [str(question_id)] = correct_incorrect
    
    if task =='registrar_summary':
        pass
        
    if task =='question_comparison':
        pass
    
    return dict(task=task,
                stats = the_stats,
                users = the_users, 
                questions_in_order = questions_in_order,
                site = Site.objects.get_current()
           )    
    

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



