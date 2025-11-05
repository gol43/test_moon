from pydantic import BaseModel, Field

class ActivityCreate(BaseModel):
    name: str
    parent_id: int | None = Field(
        default=None,
        description="ID родительской деятельности, если есть",
        example=None
    )


class ActivityRead(BaseModel):
    id: int
    name: str
    parent_id: int | None
    level: int

    class Config:
        orm_mode = True


class ActivityUpdate(BaseModel):
    name: str