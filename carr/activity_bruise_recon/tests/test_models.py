from django.test import TestCase
from .factories import CaseFactory, BlockFactory, ActivityStateFactory
from carr.activity_bruise_recon.models import score_on_bruise_recon


class TestCaseCase(TestCase):
    def test_str(self):
        c = CaseFactory()
        self.assertEqual(str(c), "test: \"[...]\"")


class TestBlock(TestCase):
    def test_add_form(self):
        b = BlockFactory()
        self.assertTrue('case_name' in b.add_form().fields)

    def test_edit_form(self):
        b = BlockFactory()
        self.assertTrue('case_name' in b.edit_form().fields)

    def test_edit(self):
        b = BlockFactory()
        b.edit(dict(case_name="new case name"), None)
        self.assertEqual(b.case_name, "new case name")

    def test_case(self):
        b = BlockFactory()
        c = CaseFactory(name=b.case_name)
        self.assertEqual(b.case(), c)


class TestScoreOnBruiseRecon(TestCase):
    def test_bad_student(self):
        self.assertIsNone(score_on_bruise_recon(None))

    def test_empty(self):
        a = ActivityStateFactory()
        self.assertEqual(score_on_bruise_recon(a.user), 0)

    def test_populated(self):
        json = '{"foo": {"score": 2}}'
        a = ActivityStateFactory(json=json)
        self.assertEqual(score_on_bruise_recon(a.user), 2)
