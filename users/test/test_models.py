from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='test@test.com',
            password='test12345',
            name='Test',
            surname='User'
        )

    def test_user_string_representation(self):

        self.assertEqual(
            str(self.user),
            'test@test.com'
        )

    def test_full_name_property(self):

        self.assertEqual(
            self.user.full_name,
            'Test User'
        )
