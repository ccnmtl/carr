from django.test import TestCase
from carr.activity_taking_action.tests.factories import (
    CaseFactory, BlockFactory, ActivityStateFactory)
from carr.activity_taking_action.models import score_on_taking_action


class TestCaseCase(TestCase):
    def test_unicode(self):
        c = CaseFactory()
        self.assertIsNotNone(c)


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
        self.assertEqual(b.case()[0], c)


class TestScoreOnTakingAction(TestCase):
    def test_bad_student(self):
        self.assertEqual(score_on_taking_action(None), 'no_data')

    def test_empty(self):
        a = ActivityStateFactory()
        self.assertEqual(score_on_taking_action(a.user), 'clicked_through')

    def test_populated(self):
        json = '{"complete": {"score": 2}}'
        a = ActivityStateFactory(json=json)
        self.assertEqual(score_on_taking_action(a.user), 'completed_form')
