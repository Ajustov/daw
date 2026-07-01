from django.db import models


class Seniority(models.TextChoices):
  TRAINEE = 'trainee'
  JUNIOR = 'junior'
  MID = 'mid'
  SENIOR = 'senior'
  LEAD = 'lead'
