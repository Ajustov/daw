from django.db import models


class CandidateTechnology(models.Model):
  candidate = models.ForeignKey('Candidate', on_delete=models.PROTECT)
  technology = models.ForeignKey('Technology', on_delete=models.PROTECT)

  class Meta:
    db_table = 'candidates_technologies'