from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User
from users.constants import (
    USER_LOGIN,
    USER_PASSWORD,
    USER_NAME,
    USER_SURNAME,
    OTHER_USER_LOGIN,
    OTHER_USER_NAME,
)


class UserPermissionsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email=USER_LOGIN,
            password=USER_PASSWORD,
            name=USER_NAME,
            surname=USER_SURNAME,
        )

        self.other_user = User.objects.create_user(
            email=OTHER_USER_LOGIN,
            password=USER_PASSWORD,
            name=OTHER_USER_NAME,
            surname=USER_SURNAME,
        )

    def test_guest_cannot_edit_profile(self):

        response = self.client.get(reverse("users:edit-profile"))

        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_user_can_edit_own_profile(self):

        self.client.login(email=USER_LOGIN, password=USER_PASSWORD)

        response = self.client.get(reverse("users:edit-profile"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_cannot_edit_other_profile(self):

        self.client.login(email=OTHER_USER_LOGIN, password=USER_PASSWORD)

        response = self.client.get(reverse("users:edit-profile"))

        self.assertNotEqual(response.status_code, HTTPStatus.OK)
