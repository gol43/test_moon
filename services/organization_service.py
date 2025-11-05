from fastapi import HTTPException

from schemas.organization_schemas import OrganizationCreate
from utils.repository import SQLAlchemyOrganizationRepository, SQLAlchemyRepository
from database.models import OrganizationActivity


class OrganizationService:
    def __init__(self, model):
        self.organizations_repository = SQLAlchemyOrganizationRepository(model)
        self.organizations_repository_for_action = SQLAlchemyRepository(model)
    
    async def find_organizations(self):
        return await self.organizations_repository.find_all_with_relations()

    async def find_one_organization(self, filter):
        obj = {}
        if isinstance(filter, int):
            obj['filter_key'] = 'id'
        elif isinstance(filter, str):
            obj['filter_key'] = 'name'
        else:
            raise ValueError("Invalid filter type")
        obj['filter_value'] = filter
        return await self.organizations_repository.find_one_with_relations(obj)

    async def find_organizations_by_building_id(self, building_id: int):
        obj = {}
        obj['filter_key'] = 'building_id'
        obj['filter_value'] = building_id
        return await self.organizations_repository.find_all_with_filter(obj)

    async def find_organizations_by_activity_ids(self, activity_ids: list[int]):
        return await self.organizations_repository.find_by_activity_ids(activity_ids, OrganizationActivity)
    
    async def find_organizations_in_buildings(self, building_ids: list[int]):
        return await self.organizations_repository.find_organizations_with_building_and_activities_by_building_ids(building_ids)

    async def add_organization_with_activities(self, organization: OrganizationCreate):
        organization_id = await self.organizations_repository_for_action.add_one(
            organization.model_dump(exclude={"activity_ids"}))
        
        for activity_id in organization.activity_ids:
            await self.organizations_repository.add_relation(
                table=OrganizationActivity,
                organization_id=organization_id,
                activity_id=activity_id)

        return organization_id


    async def update_organization(self, organization_id: int, organization: OrganizationCreate):
        await self.organizations_repository_for_action.update_one(
            organization_id,
            organization.model_dump(exclude={"activity_ids"}))

        await self.organizations_repository_for_action.delete_relations(
            table=OrganizationActivity,
            filter_column="organization_id",
            filter_value=organization_id)

        for activity_id in organization.activity_ids:
            await self.organizations_repository.add_relation(
                table=OrganizationActivity,
                organization_id=organization_id,
                activity_id=activity_id)

        return await self.find_one_organization(organization_id)


    async def delete_organization(self, organization_id: int):
        organization = await self.organizations_repository_for_action.find_one_with_filter({
            "filter_key": "id",
            "filter_value": organization_id})
        if not organization:
            raise HTTPException(status_code=404, detail=f"Организация с таким id: {organization_id} не найдена")

        await self.organizations_repository_for_action.delete_relations(
            table=OrganizationActivity,
            filter_column="organization_id",
            filter_value=organization_id)

        await self.organizations_repository_for_action.delete_one(organization_id)

        return {"ok": True, "deleted_id": organization_id}