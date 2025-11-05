from fastapi import HTTPException

from schemas.activity_schemas import ActivityCreate, ActivityUpdate
from utils.repository import SQLAlchemyRepository

class ActivityService:
    def __init__(self, model):
        self.activities_repository = SQLAlchemyRepository(model)
    
    async def find_activities(self):
        activities_all = await self.activities_repository.find_all()
        return activities_all

    async def find_one_activity(self, filter):
        obj = {}
        obj['filter_key'] = 'id'
        obj['filter_value'] = filter
        activity = await self.activities_repository.find_one_with_filter(obj)
        return activity
    
    async def add_activity(self, activity: ActivityCreate) -> int:
        level = 1
        if activity.parent_id is not None:
            parent_activity = await self.find_one_activity(activity.parent_id)
            if not parent_activity:
                raise HTTPException(status_code=404, detail="Родитель активности не найден")
            if parent_activity.level >= 3:
                raise HTTPException(status_code=400, detail="Превышен уровень вложенности")
            level = parent_activity.level + 1

        activity_dict = activity.model_dump()
        activity_dict['level'] = level
        activity_id = await self.activities_repository.add_one(activity_dict)
        return activity_id

    async def update_activity(self, activity_id: int, activity: ActivityUpdate) -> int:
        try:
            return await self.activities_repository.update_one(activity_id, activity.model_dump())
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    async def delete_activity(self, activity_id: int):
        try:
            await self.activities_repository.delete_one(activity_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    async def find_activities_by_name(self, filter):
        obj = {}
        obj['filter_key'] = 'name'
        obj['filter_value'] = filter
        activities = await self.activities_repository.find_all_with_filter(obj)
        return activities

    async def find_activities_by_ids(self, ids: list[int]):
        if not ids:
            return []
        activities = await self.activities_repository.find_all_with_filter_in(
            column_name="id",
            values=set(ids),
            table=self.activities_repository.model
        )
        return activities