from pydantic import BaseModel, Field

class Coordinates(BaseModel):
    lat: float = Field(..., description="Широта")
    lon: float = Field(..., description="Долгота")

    @classmethod
    def from_str(cls, s: str):
        lat, lon = map(float, s.split(","))
        return cls(lat=lat, lon=lon)

    def to_str(self) -> str:
        return f"{self.lat},{self.lon}"


class BuildingCreate(BaseModel):
    address: str
    coordinates: Coordinates


class BuildingRead(BaseModel):
    id: int
    address: str
    coordinates: Coordinates

    class Config:
        orm_mode = True
