import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
