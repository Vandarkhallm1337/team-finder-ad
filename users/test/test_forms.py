from django.test import TestCase
from users.forms import RegisterForm


class RegisterFormTest(TestCase):

    def test_valid_form(self):

        form_data = {
            'email': 'test@test.com',
            'name': 'John',
            'surname': 'Doe',
            'password': 'StrongPassword123',
        }

        form = RegisterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_wrong_email(self):

        form_data = {
            'email': '111',
            'name': 'John',
            'surname': 'Doe',
            'password': '12345678',
        }

        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_email_required(self):

        form_data = {
            'password': '12345678',
        }

        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
