from json import dumps
import unittest

from django.contrib.auth.models import Group
from django.urls.base import reverse
from django.test import TestCase, Client

from carr.carr_main.tests.factories import UserFactory, GroupFactory, \
    HierarchyFactory
from carr.quiz.models import Quiz, Question, Answer, ActivityState
from carr.quiz.scores import can_see_scores, year_range, sort_courses, \
    push_time, to_python_date, course_label, course_section, quiz_dict, \
    score_on_all_quizzes, pre_and_post_test_results, all_answers_for_quizzes, \
    count_pretest_and_posttest_students, question_and_quiz_keys, \
    has_dental_affiliation, PostTestAnalysisView


class TestFunctions(unittest.TestCase):
    def test_can_see_scores(self):
        u = UserFactory()
        u.groups.add(GroupFactory(name='tlcxml'))
        self.assertTrue(can_see_scores(u))

    def test_year_range(self):
        self.assertTrue(len(year_range()) > 0)

    def test_sort_courses(self):
        unsorted_courses = [
            dict(course_label='b', course_section='c'),
            dict(course_label='b', course_section='b'),
            dict(course_label='a', course_section='a')
        ]

        sorted_courses = [
            dict(course_label='a', course_section='a'),
            dict(course_label='b', course_section='b'),
            dict(course_label='b', course_section='c')
        ]

        results = sort_courses(unsorted_courses)
        self.assertEqual(sorted_courses, results)

    def test_pushtime(self):
        t = []
        push_time(t)
        self.assertEqual(len(t), 1)

    def test_to_python_date(self):
        s = "Fri Dec 13 2013 20:09:27"
        r = to_python_date(s)
        self.assertEqual(r.year, 2013)

        s = "Fri Dec 13 20:09:27"
        r = to_python_date(s)
        self.assertEqual(r.year, 1900)

    def test_course_label(self):
        ci = [None, None, None, "a", "b"]
        self.assertEqual(course_label(ci), "ab")

    def test_course_section(self):
        ci = [None, None, "a"]
        self.assertEqual(course_section(ci), "a")

    def test_quiz_dict(self):
        q = dict(submit_time=[1], all_correct=2, score=3)
        self.assertEqual(quiz_dict(q), (2, 3, 1))
        q = dict(all_correct=2, score=3)
        self.assertEqual(quiz_dict(q), (2, 3))
        q = dict(score=3)
        self.assertEqual(quiz_dict(q), ('f', 3))

    def test_has_dental_affiliation(self):
        dental_user = UserFactory()
        ssw_user = UserFactory()

        dental_group = Group.objects.create(
            name='t1.y2012.s082.cd6025.intc.st.course:columbia.edu')
        ssw_group = Group.objects.create(
            name='t1.y2004.s001.ct6009.socw.st.course:columbia.edu')
        all_cu = Group.objects.create(
            name='ALL_CUR')

        all_cu.user_set.add(dental_user)
        dental_group.user_set.add(dental_user)
        self.assertTrue(has_dental_affiliation(dental_user))

        ssw_group.user_set.add(ssw_user)
        self.assertFalse(has_dental_affiliation(ssw_user))


class TestHelpers(TestCase):
    def test_score_on_all_quizzes(self):
        u = UserFactory()
        r = score_on_all_quizzes(u)
        self.assertEqual(r, [])

    def test_pre_and_post_test_results(self):
        u = UserFactory()
        r = pre_and_post_test_results(u)
        self.assertEqual(r, {'pre_test': False, 'post_test': False})

    def test_all_answers_for_quizzes(self):
        u = UserFactory()
        r = all_answers_for_quizzes(u)
        self.assertEqual(r, {})

    def test_count_pretest_and_posttest_students(self):
        u = UserFactory()
        r = count_pretest_and_posttest_students(None, [u])
        self.assertEqual(r, {'pre_test': 0, 'post_test': 0})

    def test_question_and_quiz_keys(self):
        r = question_and_quiz_keys()
        self.assertEqual(r['answer_key'], {})
        self.assertEqual(r['quiz_key'], {})
        self.assertEqual(len(r['quizzes']), 0)
        self.assertEqual(len(r['questions']), 0)


class TestViews(TestCase):
    def setUp(self):
        self.u = UserFactory(is_staff=True)
        self.u.set_password("test")
        self.u.save()
        self.c = Client()
        self.c.login(username=self.u.username, password="test")

    def test_access_list(self):
        r = self.c.get("/scores/access/")
        self.assertContains(r, "FACULTY")


class TestPostTestAnalysisView(TestCase):

    def setUp(self):
        self.quiz = Quiz.objects.create()
        self.question1 = Question.objects.create(
            quiz=self.quiz, text='foo', question_type='single choice',
            ordinality=1)
        self.correct = Answer.objects.create(
            question=self.question1, value='1', label='one thing',
            correct=True, ordinality=1)
        self.incorrect = Answer.objects.create(
            question=self.question1, value='2', label='another thing',
            ordinality=2)

        quiz_id = 'quiz_{}'.format(self.quiz.id)
        self.incorrect_state = {
            quiz_id: {
                'initial_score': {
                    'answers_given': [{
                         'answer': str(self.incorrect.id),
                         'id': str(self.question1.id)
                        }
                    ]
                }
            }
        }

        self.correct_state = {
            quiz_id: {
                'initial_score': {
                    'answers_given': [{
                         'answer': str(self.correct.id),
                         'id': str(self.question1.id)
                        }
                    ]
                }
            }
        }

        self.h = HierarchyFactory()
        root = self.h.get_root()
        section = root.append_child('One', 'one')
        section.append_pageblock('Post-test', content_object=self.quiz)

    def test_dispatch(self):
        # not logged in
        url = reverse('post-test-analysis')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # accessing as student
        student = UserFactory()
        self.client.login(username=student.username, password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # using get
        faculty = UserFactory(is_staff=True)
        self.client.login(username=faculty.username, password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_get_posttest(self):
        self.assertEqual(PostTestAnalysisView().get_posttest(), self.quiz)

    def test_correct_answer(self):
        view = PostTestAnalysisView()
        self.assertEqual(view.correct_answer_id(self.question1),
                         str(self.correct.id))

    def test_initialize(self):
        view = PostTestAnalysisView()
        results = view.initialize(self.quiz)

        key = str(self.question1.id)
        self.assertTrue(key in results)
        self.assertEqual(results[key]['id'], self.question1.id)
        self.assertEqual(results[key]['text'], 'foo')
        self.assertEqual(results[key]['answer'], str(self.correct.id))

    def test_analyze(self):
        u = UserFactory()
        ActivityState.objects.create(user=u, json=dumps(self.incorrect_state))
        u = UserFactory()
        ActivityState.objects.create(user=u, json='')
        UserFactory()

        view = PostTestAnalysisView()
        results = view.initialize(self.quiz)
        results = view.analyze(self.quiz, results)

        key = str(self.question1.id)
        self.assertEqual(results[key]['responses'], 1)
        self.assertEqual(results[key]['correct'], 0)

    def test_post(self):
        ActivityState.objects.create(user=UserFactory(),
                                     json=dumps(self.incorrect_state))
        ActivityState.objects.create(user=UserFactory(),
                                     json=dumps(self.correct_state))

        faculty = UserFactory(is_staff=True)
        self.client.login(username=faculty.username, password='test')

        url = reverse('post-test-analysis')
        response = self.client.post(url)
        self.assertContains(response, 'q1,foo,50.0')
