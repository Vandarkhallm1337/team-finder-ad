from django.test import TestCase
from projects.forms import ProjectForm


class ProjectFormTest(TestCase):

    def test_valid_form(self):

        form_data = {
            'title': 'Project',
            'description': 'Description',
            'github_url': '',
            'status': 'open',
        }

        form = ProjectForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_title_required(self):

        form_data = {
            'description': 'Description'
        }

        form = ProjectForm(data=form_data)

        self.assertFalse(form.is_valid())
