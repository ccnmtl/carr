import factory
from carr.activity_bruise_recon.models import (
    Case, Block, ActivityState)
from django.contrib.auth.models import User


class CaseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Case
    name = "test"
    case_history = ""


class BlockFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Block
    case_name = "test"


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%03d" % n)


class ActivityStateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ActivityState
    user = factory.SubFactory(UserFactory)
    json = "{}"
