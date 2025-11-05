from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload

from database.db import get_session

class AbstractRepository(ABC):
    @abstractmethod
    async def find_all():
        raise NotImplementedError
    
    @abstractmethod
    async def find_one_with_filter():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all_with_filter():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all_with_filter_in():
        raise NotImplementedError

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def add_relation():
        raise NotImplementedError
    
    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, model):
        self.model = model

    async def find_all(self):
        async with get_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()
        
    async def find_one_with_filter(self, obj):
        async with get_session() as session:
            key_filter = obj['filter_key']
            value_filter = obj['filter_value']
            stmt = select(self.model).where(getattr(self.model, key_filter) == value_filter)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_all_with_filter(self, obj: dict):
        async with get_session() as session:
            key_filter = obj['filter_key']
            value_filter = obj['filter_value']
            stmt = select(self.model).where(getattr(self.model, key_filter) == value_filter)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_all_with_filter_in(self, column_name: str, values: set, table):
        async with get_session() as session:
            stmt = select(table).where(getattr(table, column_name).in_(values))
            res = await session.execute(stmt)
            return res.scalars().all()

    async def add_one(self, data: dict) -> int:
        async with get_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        
    async def add_relation(self, table, **kwargs):
        async with get_session() as session:
            stmt = insert(table).values(**kwargs)
            await session.execute(stmt)
            await session.commit()

    async def delete_relations(self, table, filter_column, filter_value):
        async with get_session() as session:
            stmt = delete(table).where(getattr(table, filter_column) == filter_value)
            await session.execute(stmt)
            await session.commit()
            
    async def update_one(self, obj_id: int, data: dict) -> int:
        async with get_session() as session:
            exists = await session.execute(select(self.model).where(self.model.id == obj_id))
            if not exists.scalar():
                raise ValueError(f"Объект с id {obj_id} не найден")
            stmt = update(self.model).where(self.model.id == obj_id).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        
    async def delete_one(self, obj_id: int):
        async with get_session() as session:
            exists = await session.execute(select(self.model).where(self.model.id == obj_id))
            if not exists.scalar():
                raise ValueError(f"Объект с id {obj_id} не найден")
            stmt = delete(self.model).where(self.model.id == obj_id)
            await session.execute(stmt)
            await session.commit()
        

class SQLAlchemyOrganizationRepository(SQLAlchemyRepository):
    async def find_all_with_relations(self):
        async with get_session() as session:
            stmt = select(self.model).options(
                selectinload(self.model.building),
                selectinload(self.model.activities)
            )
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_one_with_relations(self, obj):
        async with get_session() as session:
            key_filter = obj['filter_key']
            value_filter = obj['filter_value']
            stmt = (
                select(self.model)
                .where(getattr(self.model, key_filter) == value_filter)
                .options(
                    selectinload(self.model.building),
                    selectinload(self.model.activities)
                )
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_by_activity_ids(self, activity_ids: list[int], table):
        async with get_session() as session:
            stmt = (
                select(self.model)
                .join(table)
                .where(table.activity_id.in_(activity_ids))
                .options(
                    selectinload(self.model.building),
                    selectinload(self.model.activities)
                )
            )
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_organizations_with_building_and_activities_by_building_ids(self, building_ids: list[int]):
        async with get_session() as session:
            stmt = select(self.model).where(self.model.building_id.in_(building_ids)) \
                .options(selectinload(self.model.building), selectinload(self.model.activities))
            res = await session.execute(stmt)
            return res.scalars().all()
