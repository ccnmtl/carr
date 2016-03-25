from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from carr.activity_taking_action.models import ActivityState, User
from carr.mixins import LoggedInMixin
from carr.utils import state_json
import json


class LoadStateView(LoggedInMixin, View):
    def get(self, request):
        response = HttpResponse(state_json(ActivityState, request.user),
                                'application/json')
        response['Cache-Control'] = 'max-age=0,no-cache,no-store'
        return response


class SaveStateView(LoggedInMixin, View):
    def post(self, request):
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


class StudentView(LoggedInMixin, View):
    template_name = 'activity_taking_action/student_response.html'

    def get(self, request, user_id):
        if request.user.user_type() == "student":
            student_user = request.user
        else:
            student_user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {
            'student': student_user,
            'student_json': state_json(ActivityState, student_user)
        })
