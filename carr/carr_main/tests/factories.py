import factory
from carr.quiz.tests.factories import UserFactory
from carr.carr_main.models import SiteState


class SiteStateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SiteState
    user = factory.SubFactory(UserFactory)
    last_location = "/"
    visited = "{}"
