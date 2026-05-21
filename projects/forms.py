from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "name",
            "description",
            "github_url",
            "status",
        ]
        labels = {
            "name": "Название проекта",
            "description": "Описание",
            "github_url": "URL репозитория Github",
            "status": "Статус проекта",
        }

    def clean_github_url(self):
        github_url = self.cleaned_data["github_url"]

        if github_url and "github.com" not in github_url:
            raise forms.ValidationError("Only Github links allowed")

        return github_url
