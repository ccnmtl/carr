from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from carr.activity_taking_action.models import ActivityState, User
from carr.mixins import LoggedInMixin, BaseLoadStateView
from carr.utils import state_json
import json


class LoadStateView(LoggedInMixin, BaseLoadStateView):
    state_class = ActivityState


class SaveStateView(LoggedInMixin, View):
    state_class = ActivityState

    def post(self, request):
        jsn = request.POST.get('json', '{}')
        update = json.loads(jsn)

        try:
            state = self.state_class.objects.get(user=request.user)

            obj = json.loads(state.json)
            for item in update:
                obj[item] = update[item]

            state.json = json.dumps(obj)
            state.save()
        except self.state_class.DoesNotExist:
            state = self.state_class.objects.create(
                user=request.user, json=jsn)

        response = {}
        response['success'] = 1

        return HttpResponse(json.dumps(response), 'application/json')


class StudentView(LoggedInMixin, View):
    template_name = 'activity_taking_action/student_response.html'
    state_class = ActivityState

    def get(self, request, user_id):
        if request.user.user_type() == "student":
            student_user = request.user
        else:
            student_user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {
            'student': student_user,
            'student_json': state_json(self.state_class, student_user)
        })
