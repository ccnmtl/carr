from django.test import TestCase
from carr.carr_main.models import (
    user_type, new_get_children)
from .factories import SiteStateFactory, SiteSectionFactory


class SimpleModelTest(TestCase):
    def test_user_type(self):
        r = user_type(None)
        self.assertEqual(r, None)


class DummySection(object):
    id = 1
    label = "one"

    def section_site(self):
        class has_all(object):
            def all(self):
                return []

        class f(object):
            sites = has_all()

        return f()


class SiteStateTest(TestCase):
    def test_create(self):
        SiteStateFactory()
        SiteStateFactory(visited="")

    def test_get_has_visited(self):
        s = SiteStateFactory()
        self.assertFalse(s.get_has_visited(DummySection()))

    def test_set_has_visited(self):
        s = SiteStateFactory()
        s.set_has_visited([DummySection()])
        self.assertTrue(s.get_has_visited(DummySection()))

    def test_save_last_location(self):
        s = SiteStateFactory()
        s.save_last_location("/foo/", DummySection())
        self.assertFalse(s.get_has_visited(DummySection()))
        self.assertEqual(s.last_location, "/")


class SiteSectionTest(TestCase):
    def test_create(self):
        SiteSectionFactory()

    def test_unicode(self):
        s = SiteSectionFactory()
        self.assertEqual(str(s), s.label)

    def test_new_get_children(self):
        s = SiteSectionFactory()
        self.assertEqual(new_get_children(s), [])
