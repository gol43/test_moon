from pydantic import BaseModel
from schemas.activity_schemas import ActivityRead
from schemas.buildings_schemas import BuildingRead

class OrganizationCreate(BaseModel):
    name: str
    phones: list[str] | None
    building_id: int
    activity_ids: list[int]


class OrganizationRead(BaseModel):
    id: int
    name: str
    phones: list[str] | None
    building: BuildingRead
    activities: list[ActivityRead]

    class Config:
        orm_mode = True
