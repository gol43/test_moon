from fastapi import HTTPException

from schemas.buildings_schemas import BuildingCreate
from utils.repository import SQLAlchemyRepository

class BuildingService:
    def __init__(self, model):
        self.buildings_repository = SQLAlchemyRepository(model)
    
    async def find_buildings(self):
        buildings_all = await self.buildings_repository.find_all()
        return buildings_all

    async def find_one_building(self, filter):
        obj = {}
        obj['filter_key'] = 'id'
        obj['filter_value'] = filter
        building = await self.buildings_repository.find_one_with_filter(obj)
        return building
    
    async def add_building(self, building: BuildingCreate) -> int:
        building_dict = building.model_dump()
        building_id = await self.buildings_repository.add_one(building_dict)
        return building_id
    
    async def delete_building(self, building_id: int):
        try:
            await self.buildings_repository.delete_one(building_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))