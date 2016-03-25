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
