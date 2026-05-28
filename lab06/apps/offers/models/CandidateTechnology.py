from django.db import models


class CandidateTechnology(models.Model):
  candidate_id = models.ForeignKey('Candidate', on_delete=models.PROTECT)  # type: ignore
  technology_id = models.ForeignKey('Technology', on_delete=models.PROTECT)  # type: ignore

  class Meta:
    db_table = 'candidates_technologies'
