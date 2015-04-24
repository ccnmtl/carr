import factory
from django.contrib.sites.models import Site
from carr.quiz.tests.factories import UserFactory
from carr.carr_main.models import SiteState, SiteSection
from pagetree.models import Hierarchy


class SiteStateFactory(factory.DjangoModelFactory):
    class Meta:
        model = SiteState
    user = factory.SubFactory(UserFactory)
    last_location = "/"
    visited = "{}"


class SiteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Site


class HierarchyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Hierarchy
    name = "main"
    base_url = "/"


class SiteSectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = SiteSection
    label = "test section"
    slug = "test"
    hierarchy = factory.SubFactory(HierarchyFactory)
