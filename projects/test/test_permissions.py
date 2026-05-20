from django.test import TestCase
from django.urls import reverse
from users.models import User
from projects.models import Project


class ProjectPermissionsTest(TestCase):

    def setUp(self):

        self.owner = User.objects.create_user(
            email='owner@test.com',
            password='12345',
            name='Owner',
            surname='User'
        )

        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='12345',
            name='Other',
            surname='User'
        )

        self.project = Project.objects.create(
            name='Project',
            description='Description',
            owner=self.owner
        )

    def test_guest_cannot_create_project(self):

        response = self.client.get(
            reverse('projects:create-project')
        )

        self.assertNotEqual(response.status_code, 200)

    def test_guest_cannot_join_project(self):

        response = self.client.post(
            reverse(
                'projects:toggle-participate',
                kwargs={'id': self.project.pk}
            )
        )

        self.assertNotEqual(response.status_code, 403)

    def test_owner_can_edit_project(self):

        self.client.login(
            email='owner@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.pk}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_other_user_cannot_edit_project(self):

        self.client.login(
            email='other@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.pk}
            )
        )

        self.assertNotEqual(response.status_code, 200)
