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


class ProjectViewsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email=TEST_USER_LOGIN,
            password=TEST_USER_PASSWORD,
            name=TEST_USER_NAME,
            surname=TEST_USER_SURNAME
        )

        self.project = Project.objects.create(
            name=TEST_PROJECT_NAME,
            description=TEST_PROJECT_DESCRIPTION,
            owner=self.user
        )

    def test_project_list_page_available(self):

        response = self.client.get(
            reverse('projects:project-list')
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_project_detail_page_available(self):

        response = self.client.get(
            reverse(
                'projects:project-detail',
                kwargs={'id': self.project.id}
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_project_requires_login(self):

        response = self.client.get(
            reverse('projects:create-project')
        )

        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_authorized_user_cannot_create_project(self):

        self.client.login(
            email=TEST_USER_LOGIN,
            password=TEST_USER_PASSWORD
        )

        response = self.client.get(
            reverse('projects:create-project')
        )

        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_owner_can_edit_project(self):

        self.client.login(
            email=TEST_USER_LOGIN,
            password=TEST_USER_PASSWORD
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.id}
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_other_user_cannot_edit_project(self):

        other_user = User.objects.create_user(
            email=TEST_USER_OTHER_LOGIN,
            password=TEST_USER_PASSWORD,
            name=TEST_USER_OTHER_NAME,
            surname='User'
        )

        self.client.login(
            email=TEST_USER_OTHER_LOGIN,
            password=TEST_USER_PASSWORD
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.id}
            )
        )

        self.assertNotEqual(response.status_code, HTTPStatus.OK)
