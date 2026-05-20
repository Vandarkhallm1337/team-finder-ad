import random
from io import BytesIO
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from .managers import UserManager


def generate_avatar(letter):
    img = Image.new('RGB', (200, 200), color=random.choice([
        '#FF5733', '#33C1FF', '#75FF33', '#FF33A8'
    ]))

    draw = ImageDraw.Draw(img)
    draw.text((80, 70), letter.upper(), fill='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)

    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12)

    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.avatar:
            avatar_content = generate_avatar(self.name[0])
            self.avatar.save(f'{self.email}.png', ContentFile(avatar_content),
                             save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.name} {self.surname}'
