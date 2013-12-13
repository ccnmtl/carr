from django.test import TestCase
from carr.carr_main.models import user_type


class SimpleModelTest(TestCase):
    def test_user_type(self):
        r = user_type(None)
        self.assertEqual(r, None)
