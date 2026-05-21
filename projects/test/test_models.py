from django.test import TestCase

from users.models import User
from projects.models import Project
from projects.constants import (
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
    TEST_USER_NAME,
    TEST_USER_SURNAME,
    TEST_PROJECT_DESCRIPTION,
    TEST_PROJECT_NAME
)


class ProjectModelTest(TestCase):

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

    def test_project_string_representation(self):

        self.assertEqual(
            str(self.project),
            TEST_PROJECT_NAME
        )

    def test_project_owner(self):

        self.assertEqual(
            self.project.owner,
            self.user
        )

    def test_project_default_status(self):

        self.assertFalse(
            self.project.status
        )

    def test_likes_count_property(self):

        self.user.favorites.add(self.project)

        self.assertEqual(
            self.project.likes_count,
            1
        )
