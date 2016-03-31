from carr.activity_taking_action.models import ActivityState
from carr.mixins import (
    LoggedInMixin, BaseLoadStateView, BaseSaveStateView, BaseStudentView)


class LoadStateView(LoggedInMixin, BaseLoadStateView):
    state_class = ActivityState


class SaveStateView(LoggedInMixin, BaseSaveStateView):
    state_class = ActivityState


class StudentView(LoggedInMixin, BaseStudentView):
    template_name = 'activity_taking_action/student_response.html'
    state_class = ActivityState
