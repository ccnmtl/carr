from django.contrib.sites.models import Site
from django.test import TestCase, Client
from pagetree.models import SectionChildren

from carr.carr_main.models import get_previous_site_section, \
    get_next_site_section
from carr.carr_main.tests.factories import HierarchyFactory, \
    SiteStateFactory, SiteSectionFactory, SiteFactory
from carr.carr_main.views import _unlocked, _construct_menu
from carr.quiz.models import Quiz, Question

from .factories import UserFactory


class TestViews(TestCase):
    def setUp(self):
        self.u = UserFactory()
        self.u.set_password("test")
        self.u.save()
        self.c = Client()
        self.c.login(username=self.u.username, password="test")

    def test_index(self):
        r = self.c.get("/")
        self.assertEqual(r.status_code, 302)

    def test_index_logged_in(self):
        h = HierarchyFactory()
        root = h.get_root()
        site = Site.objects.get(id=1)  # available by default.

        section1 = SiteSectionFactory(hierarchy=h, label='CARR', slug='carr')
        section1.sites.add(site)
        SectionChildren.objects.create(
            parent=root, child=section1, ordinality=1)
        section2 = SiteSectionFactory(hierarchy=h)
        section2.sites.add(site)
        SectionChildren.objects.create(
            parent=root, child=section2, ordinality=2)

        with self.settings(SITE_ID=site.id):
            ss = SiteStateFactory()
            self.client.login(username=ss.user.username, password='test')
            r = self.client.get('/', follow=True)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.redirect_chain, [('/carr', 302)])

    def test_smoketest(self):
        r = self.c.get("/smoketest/")
        self.assertEqual(r.status_code, 200)

    def test_selenium(self):
        UserFactory(username="student1")
        r = self.c.get("/selenium/setup/")
        self.assertEqual(r.status_code, 200)

    def test_stats(self):
        r = self.c.get("/stats/registrar_summary/")
        self.assertEqual(r.status_code, 302)

    def test_background(self):
        r = self.c.get("/background/about/")
        self.assertEqual(r.status_code, 200)

    def test_background_invalid(self):
        r = self.c.get("/background/foo/")
        self.assertEqual(r.status_code, 302)

    def test_add_classes_form(self):
        r = self.c.get("/add_classes/")
        self.assertEqual(r.status_code, 200)

    def test_add_classes_empty(self):
        r = self.c.post("/add_classes/", dict())
        self.assertEqual(r.status_code, 200)

        r = self.c.post("/add_classes/", dict(section_keys=''))
        self.assertEqual(r.status_code, 200)

    def test_add_classes_post(self):
        r = self.c.post("/add_classes/",
                        dict(section_keys="20121SOCW7114T005,20153SOCW0006TD21"
                             )
                        )
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "alert-success")

    def test_add_classes_invalid(self):
        r = self.c.post("/add_classes/", dict(section_keys="foo"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "alert-error")

    def test_404(self):
        r = self.c.get("/this/is/a/404/")
        self.assertEqual(r.status_code, 404)

    def test_unlocked(self):
        self.h = HierarchyFactory()
        root = self.h.get_root()
        section1 = root.append_child('One', 'one')
        section2 = root.append_child('Two', 'two')
        section3 = root.append_child('Three', 'three')

        quiz = Quiz.objects.create()
        Question.objects.create(
            quiz=quiz, text='foo', question_type='short text')
        section1.append_pageblock('child', content_object=quiz)
        site = SiteStateFactory()

        self.assertTrue(_unlocked(None, site.user, None, site))
        self.assertTrue(_unlocked(section1, site.user, None, site))
        self.assertFalse(_unlocked(section2, site.user, section1, site))
        self.assertFalse(_unlocked(section3, site.user, section2, site))


class TestHierarchyNavigation(TestCase):

    def setUp(self):
        h = HierarchyFactory()
        self.root = h.get_root()
        self.site = SiteFactory()

        self.section1 = SiteSectionFactory(hierarchy=h)
        self.section1.sites.add(self.site)
        SectionChildren.objects.create(parent=self.root, child=self.section1)

        self.section2 = SiteSectionFactory(hierarchy=h)
        self.section2.sites.add(self.site)
        SectionChildren.objects.create(parent=self.root, child=self.section2)

        self.section3 = SiteSectionFactory(hierarchy=h)
        self.section3.sites.add(self.site)
        SectionChildren.objects.create(parent=self.root, child=self.section3)

        self.section4 = SiteSectionFactory(hierarchy=h)
        SectionChildren.objects.create(parent=self.root, child=self.section4)

        self.ss = SiteStateFactory()

    def test_construct_menu(self):
        with self.settings(SITE_ID=self.site.id):
            menu = _construct_menu(
                self.ss.user, self.root, self.section3, self.ss)
            self.assertEquals(len(menu), 3)

            self.assertEquals(menu[0]['section'].label, self.section1.label)
            self.assertTrue(menu[0]['accessible'])

            self.assertEquals(menu[1]['section'].label, self.section2.label)
            self.assertFalse(menu[1]['accessible'])

            self.assertEquals(menu[2]['section'].label, self.section3.label)
            self.assertFalse(menu[2]['accessible'])
            self.assertTrue(menu[2]['selected'])

    def test_hierarchy_navigation(self):
        with self.settings(SITE_ID=self.site.id):
            kids = self.root.get_children()
            self.assertEquals(len(kids), 3)
            self.assertEquals(kids[0].sitesection, self.section1)
            self.assertEquals(kids[1].sitesection, self.section2)
            self.assertEquals(kids[2].sitesection, self.section3)

            sibs = self.section1.get_siblings()
            self.assertEquals(len(sibs), 3)
            self.assertEquals(sibs[0].sitesection, self.section1)
            self.assertEquals(sibs[1].sitesection, self.section2)
            self.assertEquals(sibs[2].sitesection, self.section3)

            self.assertEquals(
                get_previous_site_section(self.section2), self.section1)
            self.assertEquals(
                get_next_site_section(self.section1), self.section2)
            self.assertIsNone(get_next_site_section(self.section3))
            self.assertIsNone(get_previous_site_section(self.section1))
