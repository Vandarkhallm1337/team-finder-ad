from django.db import models
from django.conf import settings

from projects.constants import (
    STATUS_CHOICES,
    MAX_LENGTH_NAME,
    MAX_LENGTH_STATUS,
    STATUS_OPEN_LOWER
)

User = settings.AUTH_USER_MODEL


class Project(models.Model):

    name = models.CharField(max_length=MAX_LENGTH_NAME)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    github_url = models.URLField(blank=True, null=True)

    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=STATUS_CHOICES
    )

    participants = models.ManyToManyField(
        User,
        related_name='participated_projects',
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def author(self):
        return self.owner

    @property
    def members_count(self):
        return self.participants.count()

    @property
    def likes_count(self):
        return self.interested_users.count()

    @property
    def is_open(self):
        return self.status == STATUS_OPEN_LOWER
