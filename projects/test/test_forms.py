from django.test import TestCase

from projects.forms import ProjectForm
from projects.constants import (
    TEST_PROJECT_NAME,
    TEST_PROJECT_DESCRIPTION,
    STATUS_OPEN_LOWER,
)


class ProjectFormTest(TestCase):

    def test_valid_form(self):

        form_data = {
            "title": TEST_PROJECT_NAME,
            "description": TEST_PROJECT_DESCRIPTION,
            "github_url": "",
            "status": STATUS_OPEN_LOWER,
        }

        form = ProjectForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_title_required(self):

        form_data = {"description": TEST_PROJECT_DESCRIPTION}

        form = ProjectForm(data=form_data)

        self.assertFalse(form.is_valid())
