from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from carr.activity_bruise_recon.models import ActivityState, User, Block
from carr.utils import state_json
import json


@login_required
def loadstate(request):
    response = HttpResponse(state_json(ActivityState, request.user),
                            'application/json')
    response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return response


@login_required
def savestate(request):
    jsn = request.POST['json']
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
def student(request, block_id, user_id):

    if request.user.user_type() == "student":
        student_user = request.user
    else:
        student_user = get_object_or_404(User, id=user_id)

    block = Block.objects.get(pk=block_id)
    return render(request, 'activity_bruise_recon/student_response.html', {
        'student': student_user,
        'bruise_recon_block': block,
        'student_json': state_json(ActivityState, student_user)
    })
