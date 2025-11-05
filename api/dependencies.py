from services.activity_service import ActivityService
from services.building_service import BuildingService
from services.organization_service import OrganizationService

from database.models import Activity, Building, Organization


def activities_service():
    return ActivityService(Activity)


def buildings_service():
    return BuildingService(Building)


def organizations_service():
    return OrganizationService(Organization)