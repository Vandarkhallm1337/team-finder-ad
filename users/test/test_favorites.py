from django.test import TestCase
from django.urls import reverse

from users.models import User
from projects.models import Project
from users.constants import (
    USER_LOGIN,
    USER_PASSWORD,
    USER_NAME,
    USER_SURNAME,
    OTHER_USER_LOGIN,
    OTHER_USER_NAME,
    STATUS_OPEN,
    PROJECT_NAME,
    PROJECT_DESCRIPTION,
)


class FavoriteProjectsTest(TestCase):

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

        self.project = Project.objects.create(
            name=PROJECT_NAME,
            description=PROJECT_DESCRIPTION,
            owner=self.user,
            status=STATUS_OPEN,
        )

    def test_add_project_to_favorites(self):
        self.user.favorites.add(self.project)

        self.client.login(email=USER_LOGIN, password=USER_PASSWORD)

        self.client.post(
            reverse("projects:toggle-favorite", kwargs={"id": self.project.id})
        )

        self.assertIn(self.project, self.user.favorites.all())

    def test_remove_project_from_favorites(self):

        self.user.favorites.remove(self.project)

        self.client.login(email=USER_LOGIN, password=USER_PASSWORD)

        self.client.post(
            reverse("projects:toggle-favorite", kwargs={"id": self.project.id})
        )

        self.assertNotIn(self.project, self.user.favorites.all())
