from django.shortcuts import render
from carr.activity_bruise_recon.models import ActivityState, Block
from carr.mixins import (
    LoggedInMixin, BaseLoadStateView, BaseSaveStateView, BaseStudentView)
from carr.utils import state_json


class LoadStateView(LoggedInMixin, BaseLoadStateView):
    state_class = ActivityState


class SaveStateView(LoggedInMixin, BaseSaveStateView):
    state_class = ActivityState


class StudentView(LoggedInMixin, BaseStudentView):
    template_name = 'activity_bruise_recon/student_response.html'
    state_class = ActivityState

    def get(self, request, block_id, user_id):
        student_user = self.get_student_user(request, user_id)
        block = Block.objects.get(pk=block_id)
        return render(request, self.template_name, {
            'student': student_user,
            'bruise_recon_block': block,
            'student_json': state_json(ActivityState, student_user)
        })
