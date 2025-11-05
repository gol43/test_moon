from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List

from schemas.organization_schemas import OrganizationCreate, OrganizationRead
from services.organization_service import OrganizationService
from services.activity_service import ActivityService
from services.building_service import BuildingService
from api.dependencies import organizations_service, activities_service, buildings_service

organization_router = APIRouter()


@organization_router.get('/by_geo', response_model=List[OrganizationRead])
async def get_organizations_in_box(lat_min: float,
                                   lon_min: float,
                                   lat_max: float,
                                   lon_max: float,
                                   organization_service: Annotated[OrganizationService, Depends(organizations_service)],
                                   building_service: Annotated[BuildingService, Depends(buildings_service)]):
    
    buildings = await building_service.find_buildings()
    buildings_in_box = [
        b for b in buildings
        if lat_min <= b.coordinates['lat'] <= lat_max
        and lon_min <= b.coordinates['lon'] <= lon_max
    ]
    if not buildings_in_box:
        return []

    building_ids = [b.id for b in buildings_in_box]
    organizations = await organization_service.find_organizations_in_buildings(building_ids)
    return organizations


@organization_router.get('/get_all_organizations', response_model=List[OrganizationRead])
async def get_all_organizations(organization_service: Annotated[OrganizationService, Depends(organizations_service)]):
    return await organization_service.find_organizations()


@organization_router.post('/create_organization')
async def create_organization(organization_in: OrganizationCreate,
                              organization_service: Annotated[OrganizationService, Depends(organizations_service)],
                              building_service: Annotated[BuildingService, Depends(buildings_service)],
                              activity_service: Annotated[ActivityService, Depends(activities_service)]):
    
    building = await building_service.find_one_building(organization_in.building_id)
    if not building:
        raise HTTPException(status_code=400, detail=f"Здание с таким id: {organization_in.building_id} не найдено")

    activities = await activity_service.find_activities_by_ids(organization_in.activity_ids)
    found_ids = {a.id for a in activities}
    missing_ids = set(organization_in.activity_ids) - found_ids
    if missing_ids:
        raise HTTPException(status_code=400, detail=f"Активность с таким id: {missing_ids} не найдена")

    organization_id = await organization_service.add_organization_with_activities(organization_in)
    return {"ok": True, "created_id": organization_id}


@organization_router.put('/update/{organization_id}', response_model=OrganizationRead)
async def update_organization(organization_id: int,
                              organization_in: OrganizationCreate,
                              organization_service: Annotated[OrganizationService, Depends(organizations_service)],
                              building_service: Annotated[BuildingService, Depends(buildings_service)],
                              activity_service: Annotated[ActivityService, Depends(activities_service)]):
    
    building = await building_service.find_one_building(organization_in.building_id)
    if not building:
        raise HTTPException(status_code=400, detail=f"Здание с таким id: {organization_in.building_id} не найдено")

    activities = await activity_service.find_activities_by_ids(organization_in.activity_ids)
    found_ids = {a.id for a in activities}
    missing_ids = set(organization_in.activity_ids) - found_ids
    if missing_ids:
        raise HTTPException(status_code=400, detail=f"Активность с таким id: {missing_ids} не найдена")

    updated_org = await organization_service.update_organization(organization_id, organization_in)
    return updated_org


@organization_router.delete('/delete/{organization_id}')
async def delete_organization(organization_id: int,
                              organization_service: Annotated[OrganizationService, Depends(organizations_service)]):
    result = await organization_service.delete_organization(organization_id)
    return result


@organization_router.get('/{organization_id}', response_model=OrganizationRead)
async def get_organization_by_id(organization_id: int,
                                 organization_service: Annotated[OrganizationService, Depends(organizations_service)]):
    org = await organization_service.find_one_organization(organization_id)
    return org


@organization_router.get('/by_name/{name}', response_model=OrganizationRead)
async def get_organization_by_name(name: str,
                                   organization_service: Annotated[OrganizationService, Depends(organizations_service)]):
    org = await organization_service.find_one_organization(name)
    return org


@organization_router.get('/by_activity_name/{activity_name}', response_model=List[OrganizationRead])
async def search_organizations_by_activity_tree(activity_name: str,
                                                organization_service: Annotated[OrganizationService, Depends(organizations_service)],
                                                activity_service: Annotated[ActivityService, Depends(activities_service)]):
    activities = await activity_service.find_activities_by_name(activity_name)
    if not activities:
        return []

    activity_ids = [a.id for a in activities]
    organizations = await organization_service.find_organizations_by_activity_ids(activity_ids)
    return organizations


@organization_router.get('/by_activity_id/{activity_id}', response_model=List[OrganizationRead])
async def get_organizations_by_activity(activity_id: int,
                                        organization_service: Annotated[OrganizationService, Depends(organizations_service)]):
    organizations = await organization_service.find_organizations_by_activity_ids([activity_id])
    return organizations


@organization_router.get('/get_organizations_by_building/{building_id}')
async def get_organizations_by_building(building_id: int,
                                        organization_service: Annotated[OrganizationService, Depends(organizations_service)]):
    result = await organization_service.find_organizations_by_building_id(building_id)
    return result