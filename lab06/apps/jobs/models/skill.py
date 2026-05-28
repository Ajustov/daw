from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

from .technology import Technology
from .job import Job


class Skill(models.Model):

    class Level(models.TextChoices):
        BASIC = "basic", "Basic"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        EXPERT = "expert", "Expert"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="skills"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="required_skills"
    )

    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        blank=True,
        null=True
    )

    required = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "skills"

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["job"]),
        ]

    def clean(self):

        if self.user and self.job:
            raise ValidationError(
                "Skill cannot belong to both user and job."
            )

        if not self.user and not self.job:
            raise ValidationError(
                "Skill must belong to a user or a job."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):

        owner = self.user or self.job

        return (
            f"{self.technology.name} - "
            f"{owner}"
        )