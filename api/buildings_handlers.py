from fastapi import APIRouter, Depends
from typing import Annotated

from schemas.buildings_schemas import BuildingCreate, BuildingRead
from services.building_service import BuildingService
from api.dependencies import buildings_service

buildings_router = APIRouter()


@buildings_router.get('/get_all_buildings', response_model=list[BuildingRead])
async def get_all_buildings(building_service: Annotated[BuildingService, Depends(buildings_service)]):
    return await building_service.find_buildings()


@buildings_router.post('/create_building')
async def create_building(building_in: BuildingCreate,
                          building_service: Annotated[BuildingService, Depends(buildings_service)]):
    building_id = await building_service.add_building(building_in)
    return {"ok": True, "created_id": building_id}


@buildings_router.delete('/{building_id}')
async def delete_building(building_id: int,
                          building_service: Annotated[BuildingService, Depends(buildings_service)]):
    await building_service.delete_building(building_id)
    return {"ok": True, "deleted_id": building_id}
