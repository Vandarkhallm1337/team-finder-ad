from django.test import TestCase

from users.forms import RegisterForm
from users.constants import (
    USER_LOGIN,
    USER_PASSWORD,
    USER_NAME,
    USER_SURNAME,
    USER_WRONG_MAIL
)


class RegisterFormTest(TestCase):

    def test_valid_form(self):

        form_data = {
            'email': USER_LOGIN,
            'name': USER_NAME,
            'surname': USER_SURNAME,
            'password': USER_PASSWORD,
        }

        form = RegisterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_wrong_email(self):

        form_data = {
            'email': USER_WRONG_MAIL,
            'name': USER_NAME,
            'surname': USER_SURNAME,
            'password': USER_PASSWORD,
        }

        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_email_required(self):

        form_data = {
            'password': USER_PASSWORD,
        }

        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
