import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from carr.utils import state_json


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class BaseLoadStateView(View):
    state_class = None  # this must be overridden

    def get(self, request):
        response = HttpResponse(state_json(self.state_class, request.user),
                                'application/json')
        response['Cache-Control'] = 'max-age=0,no-cache,no-store'
        return response


class BaseSaveStateView(View):
    state_class = None  # this must be overridden

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


class BaseStudentView(View):
    template_name = None  # these must be overridden
    state_class = None

    def get_student_user(self, request, user_id):
        if request.user.user_type() == "student":
            return request.user
        else:
            return get_object_or_404(User, id=user_id)

    def get_context_data(self, request, user_id):
        student_user = self.get_student_user(request, user_id)
        return {
            'student': student_user,
            'student_json': state_json(self.state_class, student_user)
        }

    def get(self, request, user_id):
        return render(request, self.template_name,
                      self.get_context_data(request, user_id))
