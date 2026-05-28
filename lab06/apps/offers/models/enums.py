from django.db import models


class Seniority(models.TextChoices):
  JUNIOR = 'junior'
  MID = 'mid'
  SENIOR = 'senior'
  LEAD = 'lead'
