import unittest
from carr.quiz.scores import (
    can_see_scores, year_range, sort_courses, push_time,
    to_python_date, course_label, course_section,
    quiz_dict)


class DummyUser(object):
    def is_authenticated(self):
        return True

    def user_type(self):
        return 'admin'


class TestFunctions(unittest.TestCase):
    def test_can_see_scores(self):
        u = DummyUser()
        self.assertTrue(can_see_scores(u))

    def test_year_range(self):
        self.assertTrue(len(year_range()) > 0)

    def test_sort_courses(self):
        courses = [dict(course_label='a', course_section='a'),
                   dict(course_label='b', course_section='b'),
                   dict(course_label='b', course_section='c')]
        results = sort_courses(courses)
        self.assertEqual(courses, results)

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
