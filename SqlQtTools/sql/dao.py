import json
from asyncio import run
from typing import Generic

from sqlalchemy import text, select

from SqlQtTools.sql.model import async_session_maker
from SqlQtTools.sql import SQLTableMap


class SysBaseDAO(Generic[SQLTableMap]):
    """Базовый класс Data Access Object"""
    model: type[SQLTableMap]

    @staticmethod
    def construct(table_name):
        for subclass in SysBaseDAO.__subclasses__():
            if subclass.model.__name__ == table_name:
                return subclass
        raise ValueError(f"Для таблицы {table_name} не реализован класс DAO")

    # Methods UPDATE
    @classmethod
    def update(cls, entity) -> SQLTableMap:
        """Метод обновления записи
        :param entity: объект типа SysBaseTable
        """
        return cls._after_update(run(cls._update_async(cls._before_update(entity))))

    @classmethod
    def _before_update(cls, entity):
        return entity

    @classmethod
    def _after_update(cls, entity):
        return entity

    @classmethod
    async def _update_async(cls, entity):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(entity)
                # await session.merge(entity)
                await session.commit()
        return entity

    # Methods INSERT
    @classmethod
    def insert(cls, entity) -> SQLTableMap:
        return cls._after_insert(run(cls._insert_async(cls._before_insert(entity))))

    @classmethod
    def _before_insert(cls, entity):
        return entity

    @classmethod
    def _after_insert(cls, entity):
        return entity

    @classmethod
    async def _insert_async(cls, entity) -> SQLTableMap:
        async with async_session_maker() as session:
            async with session.begin():
                session.add(entity)
                await session.commit()
                return entity

    # Methods DELETE
    @classmethod
    def delete(cls, entity):
        run(cls._delete_async(cls._before_delete(entity)))
        cls._after_delete(entity)

    @classmethod
    def _before_delete(cls, entity):
        return entity

    @classmethod
    def _after_delete(cls, entity):
        return entity

    @classmethod
    async def _delete_async(cls, entity):
        async with async_session_maker() as session:
            await session.execute(text("PRAGMA foreign_keys=ON"))
            await session.delete(entity)
            await session.commit()

    # Methods QUERY и SELECT (All records) и FIND (Only a record)
    @classmethod
    def query(cls, *criteria, **filter_by):
        query = select(cls.model)
        if criteria:
            query = query.filter(*criteria)
        if filter_by:
            query = query.filter_by(**filter_by)
        return cls._after_query(query)

    @classmethod
    def _after_query(cls, query):
        return query

    @classmethod
    def select(cls, query=None):
        """Select all records"""
        query = cls.query() if query is None else query
        return run(cls._select_async(query))

    @classmethod
    def find(cls, query=None):
        """Select only a record"""
        query = cls.query() if query is None else query
        return run(cls._select_async(query, only_one=True))

    @classmethod
    async def _select_async(cls, query, only_one=False):
        async with async_session_maker() as session:
            result = await session.execute(query)
            if only_one:
                return result.scalar_one_or_none()
            else:
                return result.scalars().all()

    # Methods for PyQt
    @classmethod
    def header_by_fields(cls, fields):
        return [field.doc for field in fields]

    # Method JSON Serialize
    @classmethod
    def dict_to_json(cls, value) -> str:
        return json.dumps(value)

    @classmethod
    def json_to_dict(cls, value) -> {}:
        return json.loads(value) if value else None
