import asyncio
from sqlalchemy import text
from database.db import get_session
from database.models import Building, Activity, Organization, OrganizationActivity

async def seed_data():
    async with get_session() as session:
        await session.execute(text("DELETE FROM organization_activities;"))
        await session.execute(text("DELETE FROM organizations;"))
        await session.execute(text("DELETE FROM activities;"))
        await session.execute(text("DELETE FROM buildings;"))

        building1 = Building(id=1, address="ул. Ленина, д.1", coordinates={"lat": 54.7104, "lon": 20.5110})
        building2 = Building(id=2, address="ул. Пушкина, д.5", coordinates={"lat": 54.7200, "lon": 20.5200})
        building3 = Building(id=3, address="ул. Гагарина, д.10", coordinates={"lat": 54.7300, "lon": 20.5300})
        session.add_all([building1, building2, building3])

        activity1 = Activity(id=1, name="IT Services", level=1)
        activity2 = Activity(id=2, name="Consulting", level=1)
        activity3 = Activity(id=3, name="Web Development", level=2, parent=activity1)
        activity4 = Activity(id=4, name="Marketing", level=1)
        activity5 = Activity(id=5, name="Design", level=2, parent=activity4)
        activity6 = Activity(id=6, name="Finance", level=1)
        activities = [activity1, activity2, activity3, activity4, activity5, activity6]
        session.add_all(activities)

        org1 = Organization(id=1, name="Орг1", phones=["+70001112233"], building=building1, activities=[activity1, activity3])
        org2 = Organization(id=2, name="Орг2", phones=["+70004445566"], building=building2, activities=[activity2])
        org3 = Organization(id=3, name="Орг3", phones=["+70007778899"], building=building3, activities=[activity4, activity5, activity6])
        session.add_all([org1, org2, org3])

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_data())
