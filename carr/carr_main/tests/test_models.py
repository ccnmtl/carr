from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase

from carr.carr_main.models import user_type, new_get_children

from .factories import (SiteStateFactory, SiteSectionFactory, SectionFactory,
                        UserFactory, GroupFactory)


class SimpleModelTest(TestCase):
    def test_user_type(self):
        self.assertEqual(user_type(None), None)

        u = UserFactory()
        self.assertEqual(user_type(u), 'student')

        u = UserFactory(is_staff=True)
        self.assertEqual(user_type(u), 'faculty')

        u = UserFactory()
        with self.settings(DEFAULT_SOCIALWORK_FACULTY_UNIS=[u.username]):
            self.assertEqual(user_type(u), 'faculty')

        u = UserFactory()
        u.groups.add(GroupFactory(name='tlcxml'))
        self.assertEqual(user_type(u), 'admin')

        u = UserFactory()
        u.groups.add(GroupFactory(name='t1.y2010.s001.cf1000.scnc.fc.course'))
        self.assertEqual(user_type(u), 'faculty')


class SiteStateTest(TestCase):
    def test_create(self):
        SiteStateFactory()
        SiteStateFactory(visited="")

    def test_get_has_visited(self):
        s = SiteStateFactory()
        self.assertFalse(s.get_has_visited(SectionFactory()))

    def test_set_has_visited(self):
        s = SiteStateFactory()
        s2 = SectionFactory()
        s.set_has_visited([s2])
        self.assertTrue(s.get_has_visited(s2))

    def test_save_last_location(self):
        s = SiteStateFactory()
        s2 = SectionFactory()
        s3 = SectionFactory(hierarchy=s2.hierarchy)
        s.save_last_location("/foo/", s2)
        self.assertFalse(s.get_has_visited(s3))
        self.assertEqual(s.last_location, "/foo/")


class SiteSectionTest(TestCase):

    def test_unicode(self):
        s = SiteSectionFactory()
        self.assertEqual(str(s), s.label)

    def test_new_get_children(self):
        s = SiteSectionFactory()
        self.assertEqual(new_get_children(s), [])

    def test_site_section_nav_dummy_traversal(self):
        s = SiteSectionFactory()
        # give it a traversal function that bypasses the loop
        self.assertIsNone(s.site_section_nav(lambda x: None))

    def test_site_section_nav_fixed_traversal(self):
        s = SiteSectionFactory()
        s2 = SiteSectionFactory()
        site = Site.objects.get(id=settings.SITE_ID)
        s2.sites.add(site)
        # give it a traversal function that returns a valid result
        self.assertEqual(s.site_section_nav(lambda x: s2), s2)
