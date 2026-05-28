from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

from .job import Job


class Application(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        INTERVIEW = "interview", "Interview"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    application_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviewed_applications"
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    recruiter_comment = models.TextField(
        blank=True,
        null=True
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "applications"

        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "job"],
                name="unique_candidate_job"
            )
        ]

        indexes = [
            models.Index(fields=["candidate"])
        ]

    def clean(self):

        candidate_profile = getattr(
            self.candidate,
            "profile",
            None
        )

        if not candidate_profile:
            raise ValidationError(
                "Candidate profile required."
            )

        if candidate_profile.role != "candidate":
            raise ValidationError(
                "Only candidates can apply to jobs."
            )

        if self.reviewed_by:

            recruiter_profile = getattr(
                self.reviewed_by,
                "profile",
                None
            )

            if not recruiter_profile:
                raise ValidationError(
                    "Recruiter profile required."
                )

            if recruiter_profile.role != "recruiter":
                raise ValidationError(
                    "Only recruiters can review applications."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"