from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from carr.activity_bruise_recon.models import * 
from django.utils import simplejson


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
    #import pdb
    #pdb.set_trace()
    json = request.POST['json']
    update = simplejson.loads(json)
    
    try: 
        state = ActivityState.objects.get(user=request.user)
        
        obj = simplejson.loads(state.json)
        for item in update:
            obj[item] = update[item]
        
        state.json = simplejson.dumps(obj)
        state.save()
    except ActivityState.DoesNotExist:
        state = ActivityState.objects.create(user=request.user, json=json)
        
    response = {}
    response['success'] = 1
        
    return HttpResponse(simplejson.dumps(response), 'application/json')
    
    
@rendered_with('activity_bruise_recon/student_response.html')
def student(request, block_id, user_id):
    #/activity/bruise_recon/studentcase/3/user/5/
    student_user = get_object_or_404(User,id=user_id)
    block = Block.objects.get(pk=block_id)
    return {
        'student' : student_user,
        'bruise_recon_block': block,
        'student_json': state_json (student_user)
    }

