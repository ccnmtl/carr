from django.test import TestCase, RequestFactory
from carr.activity_bruise_recon.views import (
    LoadStateView, SaveStateView, StudentView)
from .factories import UserFactory, BlockFactory


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
        v = SaveStateView.as_view()
        response = v(r)
        self.assertEqual(response.status_code, 200)


class StudentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        u = UserFactory()
        b = BlockFactory()
        r = self.factory.get("/student")
        r.user = u
        v = StudentView.as_view()
        response = v(r, b.id, u.id)
        self.assertEqual(response.status_code, 200)
