from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserViewsTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='test@test.com',
            password='12345678',
            name='John',
            surname='Doe'
        )

    def test_register_page_available(self):

        response = self.client.get(
            reverse('users:register')
        )

        self.assertEqual(response.status_code, 200)

    def test_login_page_available(self):

        response = self.client.get(
            reverse('users:login')
        )

        self.assertEqual(response.status_code, 200)

    def test_user_list_page_available(self):

        response = self.client.get(
            reverse('users:user-list')
        )

        self.assertEqual(response.status_code, 200)

    def test_user_detail_page_available(self):
        url = reverse('users:user-details', kwargs={'id': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_profile_requires_login(self):

        response = self.client.get(
            reverse('users:edit-profile')
        )

        self.assertNotEqual(response.status_code, 200)

    def test_authorized_user_can_edit_profile(self):

        self.client.login(
            email='test@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('users:edit-profile')
        )

        self.assertEqual(response.status_code, 200)

    def test_change_password_requires_login(self):

        response = self.client.get(
            reverse('users:change-password')
        )

        self.assertNotEqual(response.status_code, 200)

    def test_authorized_user_can_open_change_password(self):

        self.client.login(
            email='test@test.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('users:change-password')
        )

        self.assertEqual(response.status_code, 200)
