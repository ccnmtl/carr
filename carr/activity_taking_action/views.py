from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from carr.activity_taking_action.models import ActivityState, User
import json
from annoying.decorators import render_to


def state_json(user):
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
    response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return response


@login_required
def savestate(request):
    jsn = request.POST.get('json', '{}')
    update = json.loads(jsn)

    try:
        state = ActivityState.objects.get(user=request.user)

        obj = json.loads(state.json)
        for item in update:
            obj[item] = update[item]

        state.json = json.dumps(obj)
        state.save()
    except ActivityState.DoesNotExist:
        state = ActivityState.objects.create(user=request.user, json=jsn)

    response = {}
    response['success'] = 1

    return HttpResponse(json.dumps(response), 'application/json')


@login_required
@render_to('activity_taking_action/student_response.html')
def student(request, user_id):
    if request.user.user_type() == "student":
        student_user = request.user
    else:
        student_user = get_object_or_404(User, id=user_id)
    return {
        'student': student_user,
        'student_json': state_json(student_user)
    }
