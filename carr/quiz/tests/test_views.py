from json import dumps, loads
from django.urls.base import reverse
from carr.carr_main.tests.factories import UserFactory, HierarchyFactory
from carr.quiz.models import Quiz, Question, Answer, ActivityState
from carr.quiz.views import studentquiz, edit_quiz, delete_question, \
    delete_answer, reorder_answers, reorder_questions, add_question_to_quiz, \
    edit_question, edit_answer, add_answer_to_question
from django.test import TestCase
from django.test.client import RequestFactory


class TestQuizViews(TestCase):

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

        self.question2 = Question.objects.create(
            quiz=self.quiz, text='bar', question_type='short text',
            ordinality=2)

        quiz_id = 'quiz_{}'.format(self.quiz.id)
        self.json_state = {
            quiz_id: {
                'all_correct': 't',
                'initial_score': {
                    'quiz_max_score': 1,
                    'quiz_score': 1
                },
                'question': [
                    {'answer': self.correct.id, 'id': self.question1.id}
                ]
            }
        }

        self.h = HierarchyFactory()
        root = self.h.get_root()
        section = root.append_child('One', 'one')
        section.append_pageblock('Quiz', content_object=self.quiz)

    def test_studentquiz(self):
        student = UserFactory()
        ActivityState.objects.create(user=student, json=dumps(self.json_state))
        request = RequestFactory().get('/')

        request.user = student
        response = studentquiz(request, self.quiz.id, request.user.id)
        self.assertEqual(response.status_code, 200)

        request.user = UserFactory(is_staff=True)
        response = studentquiz(request, self.quiz.id, student.id)
        self.assertEqual(response.status_code, 200)

    def test_edit_quiz(self):
        request = RequestFactory().get('/')
        request.user = UserFactory(is_staff=True)

        response = edit_quiz(request, self.quiz.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_question(self):
        staff = UserFactory(is_staff=True)
        request = RequestFactory().get('/')
        request.user = staff

        # are you sure view
        response = delete_question(request, self.question1.id)
        self.assertEqual(self.quiz.question_set.count(), 2)
        self.assertContains(response, 'Are you sure')

        # delete
        request = RequestFactory().post('/')
        request.user = staff
        response = delete_question(request, self.question1.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.quiz.question_set.count(), 1)

    def test_delete_answer(self):
        staff = UserFactory(is_staff=True)
        request = RequestFactory().get('/')
        request.user = staff

        # are you sure view
        response = delete_answer(request, self.correct.id)
        self.assertEqual(self.question1.answer_set.count(), 2)
        self.assertContains(response, 'Are you sure')

        # delete
        request = RequestFactory().post('/')
        request.user = staff
        response = delete_answer(request, self.correct.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.question1.answer_set.count(), 1)

    def test_reorder_answers(self):
        url = reverse('reorder-answer', args=[self.question1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.correct.ordinality, 1)
        self.assertEqual(self.incorrect.ordinality, 2)

        url = '/?answer_0={}&answer_1={}'.format(
            self.incorrect.id, self.correct.id)
        request = RequestFactory().post(url)
        request.user = UserFactory(is_staff=True)

        response = reorder_answers(request, self.question1.id)
        self.assertEqual(response.status_code, 200)

        self.correct.refresh_from_db()
        self.assertEqual(self.correct.ordinality, 2)
        self.incorrect.refresh_from_db()
        self.assertEqual(self.incorrect.ordinality, 1)

    def test_reorder_questions(self):
        url = reverse('reorder-questions', args=[self.quiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.question1.ordinality, 1)
        self.assertEqual(self.question2.ordinality, 2)

        url = '/?question_0={}&question_1={}'.format(
            self.question2.id, self.question1.id)
        request = RequestFactory().post(url)
        request.user = UserFactory(is_staff=True)

        response = reorder_questions(request, self.quiz.id)
        self.assertEqual(response.status_code, 200)

        self.question1.refresh_from_db()
        self.assertEqual(self.question1.ordinality, 2)
        self.question2.refresh_from_db()
        self.assertEqual(self.question2.ordinality, 1)

    def test_add_question_to_quiz(self):
        data = {u'text': [u'the text'],
                u'intro_text': [u'the intro'],
                u'explanation': [u'the explanation'],
                u'question_type': [u'short text']}
        request = RequestFactory().post('/', data)
        request.user = UserFactory(is_staff=True)
        response = add_question_to_quiz(request, self.quiz.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.quiz.question_set.count(), 3)

    def test_edit_question(self):
        request = RequestFactory().get('/')
        request.user = UserFactory(is_staff=True)
        response = edit_question(request, self.question2.id)
        self.assertTrue(response, 'Question 2')

    def test_edit_answer(self):
        request = RequestFactory().get('/')
        request.user = UserFactory(is_staff=True)
        response = edit_answer(request, self.incorrect.id)
        self.assertContains(response, 'Answer 2')

    def test_add_answer_to_question(self):
        data = {u'explanation': [u'the explanation'],
                u'value': [u'2'],
                u'label': [u'Maybe']}
        request = RequestFactory().post('/', data)
        request.user = UserFactory(is_staff=True)
        response = add_answer_to_question(request, self.question1.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.question1.answer_set.count(), 3)

    def test_load_state(self):
        u = UserFactory()
        state = ActivityState.objects.create(user=u,
                                             json=dumps(self.json_state))

        self.client.login(username=u.username, password='test')
        response = self.client.get('/activity/quiz/load/')
        self.assertContains(response, state.json)

    def test_save_state_created(self):
        # when no state exists
        u = UserFactory()

        self.client.login(username=u.username, password='test')

        data = {'json': dumps(self.json_state)}
        response = self.client.post('/activity/quiz/save/', data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(loads(response.content)['success'], 1)

        n = ActivityState.objects.filter(user=u, json=data['json']).count()
        self.assertEqual(n, 1)

    def test_save_state_updated(self):
        # when no state exists
        u = UserFactory()
        ActivityState.objects.create(user=u, json=dumps(self.json_state))
        self.client.login(username=u.username, password='test')

        data = {'json': '{}'}
        response = self.client.post('/activity/quiz/save/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(response.content)['success'], 1)
        n = ActivityState.objects.filter(user=u, json='{}').count()
        self.assertEqual(n, 1)
