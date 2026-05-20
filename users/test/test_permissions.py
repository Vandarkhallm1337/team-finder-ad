from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserPermissionsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='test@test.com',
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

    def test_guest_cannot_edit_profile(self):

        response = self.client.get(reverse('users:edit-profile'))

        self.assertNotEqual(response.status_code, 200)

    def test_user_can_edit_own_profile(self):

        self.client.login(
            email='user@test.com',
            password='12345678'
        )

        response = self.client.get(reverse('users:edit-profile'))

        self.assertEqual(response.status_code, 302)

    def test_user_cannot_edit_other_profile(self):

        self.client.login(
            email='other@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('users:edit-profile')
        )

        self.assertNotEqual(response.status_code, 200)
