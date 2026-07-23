import uuid

from pydantic import BaseModel


class CompanyResponseSummary(BaseModel):
  model_config = {'from_attributes': True}
  name: str


class CompanyResponseDetail(CompanyResponseSummary):
  id: uuid.UUID
