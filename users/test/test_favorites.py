from django.test import TestCase
from django.urls import reverse
from users.models import User
from projects.models import Project


class FavoriteProjectsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='user@test.com',
            password='12345',
            name='Test',
            surname='User'
        )

        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='12345',
            name='Other',
            surname='User'
        )

        self.project = Project.objects.create(
            name='Test project',
            description='Test description',
            owner=self.user,
            status='open'
        )

    def test_add_project_to_favorites(self):
        self.user.favorites.add(self.project)

        self.client.login(
            email='user@test.com',
            password='12345678'
        )

        self.client.post(
            reverse(
                'projects:toggle-favorite',
                kwargs={'id': self.project.id}
            )
        )

        self.assertIn(
            self.project,
            self.user.favorites.all()
        )

    def test_remove_project_from_favorites(self):

        self.user.favorites.remove(self.project)

        self.client.login(
            email='user@test.com',
            password='12345678'
        )

        self.client.post(
            reverse(
                'projects:toggle-favorite',
                kwargs={'id': self.project.id}
            )
        )

        self.assertNotIn(
            self.project,
            self.user.favorites.all()
        )
