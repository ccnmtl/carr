import factory

from carr.quiz.models import ActivityState


class ActivityStateFactory(factory.DjangoModelFactory):
    class Meta:
        model = ActivityState
