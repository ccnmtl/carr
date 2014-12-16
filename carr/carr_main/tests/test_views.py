from .factories import UserFactory
from django.test import TestCase, Client


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

    def test_smoketest(self):
        r = self.c.get("/smoketest/")
        self.assertEqual(r.status_code, 200)

    def test_selenium(self):
        UserFactory(username="student1")
        r = self.c.get("/selenium/setup/")
        self.assertEqual(r.status_code, 200)

    def test_stats(self):
        self.u.user_type = lambda x: 'faculty'
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
                        dict(section_keys="20121SOCW7114T005"))
        self.assertEqual(r.status_code, 200)

    def test_add_classes_invalid(self):
        r = self.c.post("/add_classes/", dict(section_keys="foo"))
        self.assertEqual(r.status_code, 200)
