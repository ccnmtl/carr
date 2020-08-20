from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
import factory
from pagetree.models import Hierarchy, Section, SectionChildren

from carr.carr_main.models import SiteState, SiteSection


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user%d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
    name = factory.Sequence(
        lambda n: 't1.y2010.s001.cf1000.scnc.st.course:%d.columbia.edu' % n)


class SiteStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SiteState
    user = factory.SubFactory(UserFactory)
    last_location = "/"
    visited = "{}"


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site


class HierarchyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hierarchy
    name = "main"
    base_url = "/"


class SiteSectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SiteSection
    label = factory.Sequence(lambda n: "test section %d" % n)
    slug = factory.Sequence(lambda n: "test%d" % n)
    hierarchy = factory.SubFactory(HierarchyFactory)


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section
    label = "test section"
    slug = "test"
    hierarchy = factory.SubFactory(HierarchyFactory)


class SectionChildrenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectionChildren
