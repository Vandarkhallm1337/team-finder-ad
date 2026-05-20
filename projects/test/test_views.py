from django.test import TestCase
from django.urls import reverse
from users.models import User
from projects.models import Project


class ProjectViewsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='test@test.com',
            password='12345',
            name='Test',
            surname='User'
        )

        self.project = Project.objects.create(
            name='Test Project',
            description='Description',
            owner=self.user
        )

    def test_project_list_page_available(self):

        response = self.client.get(
            reverse('projects:project-list')
        )

        self.assertEqual(response.status_code, 200)

    def test_project_detail_page_available(self):

        response = self.client.get(
            reverse(
                'projects:project-detail',
                kwargs={'id': self.project.id}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_create_project_requires_login(self):

        response = self.client.get(
            reverse('projects:create-project')
        )

        self.assertNotEqual(response.status_code, 200)

    def test_authorized_user_cannot_create_project(self):

        self.client.login(
            email='owner@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('projects:create-project')
        )

        self.assertNotEqual(response.status_code, 200)

    def test_owner_can_edit_project(self):

        self.client.login(
            email='owner@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.id}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_other_user_cannot_edit_project(self):

        other_user = User.objects.create_user(
            email='other@test.com',
            password='12345678',
            name='Other',
            surname='User'
        )

        self.client.login(
            email='other@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse(
                'projects:edit-project',
                kwargs={'id': self.project.id}
            )
        )

        self.assertNotEqual(response.status_code, 200)
