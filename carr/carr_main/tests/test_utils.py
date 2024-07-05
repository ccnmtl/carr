from json import dumps

from django.test.testcases import TestCase

from carr.carr_main.tests.factories import UserFactory, GroupFactory
from carr.quiz.models import ActivityState
from carr.utils import state_json, get_students, filter_users_by_affiliation


class TestUtils(TestCase):

    def test_load_quiz_state_json(self):
        some_state = {'foo': 'bar'}

        u = UserFactory()

        # no state
        self.assertEqual(state_json(ActivityState, u), '{}')

        # empty state
        state = ActivityState.objects.create(user=u, json='')
        self.assertEqual(state_json(ActivityState, u), '{}')

        state.json = dumps(some_state)
        state.save()
        self.assertEqual(state_json(ActivityState, u), state.json)

    def test_get_and_filter_students(self):
        with self.settings(DEFAULT_SOCIALWORK_FACULTY_UNIS=['ssw_faculty']):
            dental_student = UserFactory(first_name='Alpha', last_name='Beta')
            grp = 't3.y2007.s001.cw3956.intc.st.course:columbia.edu'
            dental_student.groups.add(GroupFactory(name=grp))

            ssw_student = UserFactory(first_name='Chi', last_name='Delta')

            UserFactory(is_staff=True)  # staff
            UserFactory(username='ssw_faculty')  # ssw faculty
            UserFactory().groups.add(GroupFactory(name='tlcxml'))  # admin
            UserFactory().groups.add(GroupFactory(name='a.fc.b'))  # faculty

            students = get_students()
            self.assertEqual(students.count(), 2)
            self.assertEqual(students[0], dental_student)
            self.assertEqual(students[1], ssw_student)

            qs = filter_users_by_affiliation('dental', students)
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.first(), dental_student)

            qs = filter_users_by_affiliation('ssw', students)
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.first(), ssw_student)
