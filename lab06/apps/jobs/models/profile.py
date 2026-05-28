from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

from .company import Company


class Profile(models.Model):

    class Roles(models.TextChoices):
        CANDIDATE = "candidate", "Candidate"
        RECRUITER = "recruiter", "Recruiter"

    class Seniority(models.TextChoices):
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"
        LEAD = "lead", "Lead"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        BLOCKED = "blocked", "Blocked"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profiles"
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    cv_url = models.URLField(
        blank=True,
        null=True
    )

    seniority = models.CharField(
        max_length=20,
        choices=Seniority.choices,
        blank=True,
        null=True
    )

    years_experience = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        db_table = "profiles"

    def clean(self):

        if self.role == "candidate":
            if self.company:
                raise ValidationError(
                    "Candidate cannot belong to a company."
                )

        if self.role == "recruiter":
            if not self.company:
                raise ValidationError(
                    "Recruiter must belong to a company."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username