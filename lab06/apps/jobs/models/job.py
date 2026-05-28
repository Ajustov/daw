from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

from .company import Company


class Job(models.Model):

    class Modality(models.TextChoices):
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        ONSITE = "onsite", "On Site"

    class Seniority(models.TextChoices):
        INTERN = "intern", "Intern"
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"
        LEAD = "lead", "Lead"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        PAUSED = "paused", "Paused"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=150)

    description = models.TextField()

    location = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    modality = models.CharField(
        max_length=20,
        choices=Modality.choices,
        blank=True,
        null=True
    )

    seniority = models.CharField(
        max_length=20,
        choices=Seniority.choices,
        blank=True,
        null=True
    )

    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    job_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "jobs"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["location"]),
        ]

    def clean(self):
        profile = getattr(self.recruiter, "profile", None)

        if not profile:
            raise ValidationError(
                "Recruiter profile required."
            )

        if profile.role != "recruiter":
            raise ValidationError(
                "Only recruiters can publish jobs."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title