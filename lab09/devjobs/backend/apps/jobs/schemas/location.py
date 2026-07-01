import uuid

from pydantic import BaseModel


class LocationResponseSummary(BaseModel):
  model_config = {'from_attributes': True}
  name: str


class LocationResponseDetail(LocationResponseSummary):
  id: uuid.UUID
