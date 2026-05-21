from django.test import TestCase

from users.models import User
from users.constants import (
    USER_LOGIN,
    USER_PASSWORD,
    USER_NAME,
    USER_SURNAME,
    FULL_NAME,
)


class UserModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email=USER_LOGIN,
            password=USER_PASSWORD,
            name=USER_NAME,
            surname=USER_SURNAME,
        )

    def test_user_string_representation(self):

        self.assertEqual(str(self.user), USER_LOGIN)

    def test_full_name_property(self):

        self.assertEqual(self.user.full_name, FULL_NAME)
