import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

        labels = {
            "name": "Имя",
            "surname": "псевдоним",
            "email": "почта",
            "password": "пароль",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Неверно введен логин или пароль")
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "name",
            "surname",
            "avatar",
            "about",
            "phone",
            "github_url",
        ]

        labels = {
            "name": "Имя",
            "surname": "псевдоним",
            "about": "краткие сведения",
            "phone": "телефон",
            "github_url": "URL репозитория Github",
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        pattern = r"^(\+7|8)\d{10}$"
        if not re.match(pattern, phone):
            raise forms.ValidationError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
            )

        normalized_phone = "+7" + phone[1:] if phone.startswith("8") else phone

        queryset = User.objects.filter(phone=normalized_phone)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError("Номер телефона уже используется")

        return normalized_phone

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url")

        if github_url and "github.com" not in github_url:
            raise forms.ValidationError("Ввести можно только Github-ссылку")

        return github_url


class PasswordThreePolesChangeForm(PasswordChangeForm):
    pass
