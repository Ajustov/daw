from django.db import models


class Seniority(models.TextChoices):
  TRAINEE = 'trainee'
  JUNIOR = 'junior'
  MID = 'mid'
  SENIOR = 'senior'
  LEAD = 'lead'


class Modality(models.TextChoices):
  REMOTE = 'remote'
  PRESENTIAL = 'presential'
  HYBRID = 'hybrid'


class Status(models.TextChoices):
  PENDING = 'pending'
  REVIEWED = 'reviewed'
  HIRED = 'hired'
  REJECTED = 'rejected'
