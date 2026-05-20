from django.test import TestCase

from users.models import User
from projects.models import Project


class ProjectModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='owner@test.com',
            password='12345',
            name='Project',
            surname='Owner'
        )

        self.project = Project.objects.create(
            name='Test Project',
            description='Description',
            owner=self.user
        )

    def test_project_string_representation(self):

        self.assertEqual(
            str(self.project),
            'Test Project'
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
