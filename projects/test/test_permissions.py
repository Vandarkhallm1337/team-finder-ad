from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User
from projects.models import Project
from projects.constants import (
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
    TEST_USER_NAME,
    TEST_USER_SURNAME,
    TEST_PROJECT_DESCRIPTION,
    TEST_PROJECT_NAME,
    TEST_USER_OTHER_NAME,
    TEST_USER_OTHER_LOGIN
)


class ProjectPermissionsTest(TestCase):

    def setUp(self):

        self.owner = User.objects.create_user(
            email=TEST_USER_LOGIN,
            password=TEST_USER_PASSWORD,
            name=TEST_USER_NAME,
            surname=TEST_USER_SURNAME
        )

        self.other_user = User.objects.create_user(
            email=TEST_USER_OTHER_LOGIN,
            password=TEST_USER_PASSWORD,
            name=TEST_USER_OTHER_NAME,
            surname=TEST_USER_SURNAME
        )

        self.project = Project.objects.create(
            name=TEST_PROJECT_NAME,
            description=TEST_PROJECT_DESCRIPTION,
            owner=self.owner
        )

    def test_guest_cannot_create_project(self):

        response = self.client.get(
            reverse('projects:create-project')
        )

        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_guest_cannot_join_project(self):

        response = self.client.post(
            reverse(
                'projects:toggle-participate',
                kwargs={'id': self.project.pk}
            )
        )

        self.assertNotEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_owner_can_edit_project(self):

        self.client.login(
            email=TEST_USER_LOGIN,
            password=TEST_USER_PASSWORD
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.pk}
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_other_user_cannot_edit_project(self):

        self.client.login(
            email=TEST_USER_OTHER_LOGIN,
            password=TEST_USER_PASSWORD
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.pk}
            )
        )

        self.assertNotEqual(response.status_code, HTTPStatus.OK)
