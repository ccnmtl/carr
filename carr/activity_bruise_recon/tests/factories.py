import factory
from carr.activity_bruise_recon.models import (
    Case, Block, ActivityState)
from django.contrib.auth.models import User


class CaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Case
    name = "test"
    case_history = ""


class BlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Block
    case_name = "test"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user%03d" % n)


class ActivityStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActivityState
    user = factory.SubFactory(UserFactory)
    json = "{}"
