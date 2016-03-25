from django.test import TestCase, RequestFactory
from carr.activity_taking_action.views import (
    LoadStateView, savestate, student)
from .factories import UserFactory


class LoadStateTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        u = UserFactory()
        r = self.factory.get("/loadstate")
        r.user = u
        v = LoadStateView.as_view()
        response = v(r)
        self.assertEqual(response.status_code, 200)


class SaveStateTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post(self):
        u = UserFactory()
        r = self.factory.post("/savestate", dict(json='{}'))
        r.user = u
        response = savestate(r)
        self.assertEqual(response.status_code, 200)


class StudentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        u = UserFactory()
        r = self.factory.get("/student")
        r.user = u
        response = student(r, u.id)
        self.assertEqual(response.status_code, 200)
