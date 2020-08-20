import factory

from carr.quiz.models import ActivityState


class ActivityStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActivityState
