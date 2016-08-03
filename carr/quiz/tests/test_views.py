from json import dumps

from django.test import TestCase
from django.test.client import RequestFactory

from carr.carr_main.tests.factories import UserFactory, HierarchyFactory
from carr.quiz.models import Quiz, Question, Answer, ActivityState
from carr.quiz.views import studentquiz, edit_quiz, delete_question, \
    delete_answer, reorder_answers, reorder_questions, add_question_to_quiz, \
    edit_question, edit_answer


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
        self.state = {
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
        ActivityState.objects.create(user=student, json=dumps(self.state))
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
        self.assertEquals(response.status_code, 200)

    def test_delete_question(self):
        staff = UserFactory(is_staff=True)
        request = RequestFactory().get('/')
        request.user = staff

        # are you sure view
        response = delete_question(request, self.question1.id)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.quiz.question_set.count(), 2)
        self.assertTrue('Are you sure' in response.content)

        # delete
        request = RequestFactory().post('/')
        request.user = staff
        response = delete_question(request, self.question1.id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.quiz.question_set.count(), 1)

    def test_delete_answer(self):
        staff = UserFactory(is_staff=True)
        request = RequestFactory().get('/')
        request.user = staff

        # are you sure view
        response = delete_answer(request, self.correct.id)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.question1.answer_set.count(), 2)
        self.assertTrue('Are you sure' in response.content)

        # delete
        request = RequestFactory().post('/')
        request.user = staff
        response = delete_answer(request, self.correct.id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.question1.answer_set.count(), 1)

    def test_reorder_answers(self):
        self.assertEquals(self.correct.ordinality, 1)
        self.assertEquals(self.incorrect.ordinality, 2)

        url = '/?answer_0={}&answer_1={}'.format(
            self.incorrect.id, self.correct.id)
        request = RequestFactory().post(url)
        request.user = UserFactory(is_staff=True)

        response = reorder_answers(request, self.question1.id)
        self.assertEquals(response.status_code, 200)

        self.correct.refresh_from_db()
        self.assertEquals(self.correct.ordinality, 2)
        self.incorrect.refresh_from_db()
        self.assertEquals(self.incorrect.ordinality, 1)

    def test_reorder_questions(self):
        self.assertEquals(self.question1.ordinality, 1)
        self.assertEquals(self.question2.ordinality, 2)

        url = '/?question_0={}&question_1={}'.format(
            self.question2.id, self.question1.id)
        request = RequestFactory().post(url)
        request.user = UserFactory(is_staff=True)

        response = reorder_questions(request, self.quiz.id)
        self.assertEquals(response.status_code, 200)

        self.question1.refresh_from_db()
        self.assertEquals(self.question1.ordinality, 2)
        self.question2.refresh_from_db()
        self.assertEquals(self.question2.ordinality, 1)

    def test_add_question_to_quiz(self):
        data = {u'text': [u'the text'],
                u'intro_text': [u'the intro'],
                u'explanation': [u'the explanation'],
                u'question_type': [u'short text']}
        request = RequestFactory().post('/', data)
        request.user = UserFactory(is_staff=True)
        response = add_question_to_quiz(request, self.quiz.id)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.quiz.question_set.count(), 3)

    def test_edit_question(self):
        request = RequestFactory().get('/')
        request.user = UserFactory(is_staff=True)
        response = edit_question(request, self.question2.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Question 2' in response.content)

    def test_edit_answer(self):
        request = RequestFactory().get('/')
        request.user = UserFactory(is_staff=True)
        response = edit_answer(request, self.incorrect.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Answer 2' in response.content)
