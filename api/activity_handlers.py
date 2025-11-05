from fastapi import APIRouter, Depends
from typing import Annotated

from schemas.activity_schemas import ActivityCreate, ActivityRead, ActivityUpdate
from services.activity_service import ActivityService
from api.dependencies import activities_service

activity_router = APIRouter()


@activity_router.get('/get_all_activities', response_model=list[ActivityRead])
async def get_all_activities(activity_service: Annotated[ActivityService, Depends(activities_service)]):
    return await activity_service.find_activities()


@activity_router.post('/create_activity')
async def create_activity(activity_in: ActivityCreate,
                          activity_service: Annotated[ActivityService, Depends(activities_service)]):
    activity_id = await activity_service.add_activity(activity_in)
    return {"ok": True, "created_id": activity_id}


@activity_router.put('/{activity_id}')
async def update_activity(activity_id: int,
                          activity_in: ActivityUpdate,
                          activity_service: Annotated[ActivityService, Depends(activities_service)]):
    updated_id = await activity_service.update_activity(activity_id, activity_in)
    return {"ok": True, "updated_id": updated_id}


@activity_router.delete('/{activity_id}')
async def delete_activity(activity_id: int,
                          activity_service: Annotated[ActivityService, Depends(activities_service)]):
    await activity_service.delete_activity(activity_id)
    return {"ok": True, "deleted_id": activity_id}


async def get_activities_by_name(name:str, 
                                 activity_service: Annotated[ActivityService, Depends(activities_service)]):
    result = await activity_service.find_activities_by_name(name)
    return result