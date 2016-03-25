from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from carr.activity_bruise_recon.models import ActivityState, User, Block
from carr.mixins import LoggedInMixin, BaseLoadStateView, BaseSaveStateView
from carr.utils import state_json


class LoadStateView(LoggedInMixin, BaseLoadStateView):
    state_class = ActivityState


class SaveStateView(LoggedInMixin, BaseSaveStateView):
    state_class = ActivityState


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
