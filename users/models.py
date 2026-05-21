from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile

from .managers import UserManager
from .utils import generate_avatar
from .constants import (
    MAX_LENGTH_NAME,
    MAX_LENGTH_SURNAME,
    UPLOAD_FILE,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_ABOUT,
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    surname = models.CharField(max_length=MAX_LENGTH_SURNAME)

    avatar = models.ImageField(upload_to=UPLOAD_FILE, blank=True)
    phone = models.CharField(max_length=MAX_LENGTH_PHONE)

    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=MAX_LENGTH_ABOUT, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        "projects.Project", related_name="interested_users", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.avatar:
            avatar_content = generate_avatar(self.name[0])
            self.avatar.save(
                f"{self.email}.png", ContentFile(avatar_content), save=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"
