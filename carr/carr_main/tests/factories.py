import factory
from django.contrib.sites.models import Site
from carr.quiz.tests.factories import UserFactory
from carr.carr_main.models import SiteState, SiteSection
from pagetree.models import Hierarchy


class SiteStateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SiteState
    user = factory.SubFactory(UserFactory)
    last_location = "/"
    visited = "{}"


class SiteFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Site


class HierarchyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Hierarchy
    name = "main"
    base_url = "/"


class SiteSectionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SiteSection
    label = "test section"
    slug = "test"
    hierarchy = factory.SubFactory(HierarchyFactory)
