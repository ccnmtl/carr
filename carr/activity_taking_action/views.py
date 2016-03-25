from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from carr.activity_taking_action.models import ActivityState, User
from carr.mixins import LoggedInMixin, BaseLoadStateView, BaseSaveStateView
from carr.utils import state_json


class LoadStateView(LoggedInMixin, BaseLoadStateView):
    state_class = ActivityState


class SaveStateView(LoggedInMixin, BaseSaveStateView):
    state_class = ActivityState


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
