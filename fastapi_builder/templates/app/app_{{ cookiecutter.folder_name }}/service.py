import datetime
from typing import List

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.app_{{ cookiecutter.folder_name }}.model import {{ cookiecutter.pascal_name }}
from apps.app_{{ cookiecutter.folder_name }}.schema import (
    {{ cookiecutter.pascal_name }}CreateRequest,
    {{ cookiecutter.pascal_name }}ListQueryRequest,
    {{ cookiecutter.pascal_name }}sPatchRequest,
    {{ cookiecutter.pascal_name }}UpdateRequest,
)
from core.e import ErrorCode, ErrorMessage
from schemas.base import OrderType


class {{ cookiecutter.pascal_name }}Service:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, query_params: {{ cookiecutter.pascal_name }}ListQueryRequest):
        # 获取总数
        total_count = (await self.db.execute(select(func.count()).select_from({{ cookiecutter.pascal_name }}))).scalar()

        # 查询
        stmt = await {{ cookiecutter.pascal_name }}.query()
        if query_params.size is not None:
            offset = (query_params.page - 1) * query_params.size
            stmt = stmt.offset(offset).limit(query_params.size)
        if query_params.order_type:
            stmt = stmt.order_by(
                getattr({{ cookiecutter.pascal_name }}, query_params.order_by).desc()
                if query_params.order_type == OrderType.DESC
                else getattr({{ cookiecutter.pascal_name }}, query_params.order_by).asc()
            )

        db_{{ cookiecutter.snake_name }}s: List[{{ cookiecutter.pascal_name }}] = (await self.db.execute(stmt)).scalars().all()
        
        return db_{{ cookiecutter.snake_name }}s, total_count

    async def create(self, {{ cookiecutter.snake_name }}: {{ cookiecutter.pascal_name }}CreateRequest) -> {{ cookiecutter.pascal_name }}:
        async with self.db.begin():
            db_{{ cookiecutter.snake_name }} = await {{ cookiecutter.pascal_name }}.create(self.db, **{{ cookiecutter.snake_name }}.model_dump())
        return db_{{ cookiecutter.snake_name }}

    async def patch_batch(self, {{ cookiecutter.snake_name }}s_patch_request: {{ cookiecutter.pascal_name }}sPatchRequest):
        async with self.db.begin():
            stmt = (await {{ cookiecutter.pascal_name }}.query()).filter(
                {{ cookiecutter.pascal_name }}.id.in_({{ cookiecutter.snake_name }}s_patch_request.ids)
            )
            db_{{ cookiecutter.snake_name }}s: List[{{ cookiecutter.pascal_name }}] = (await self.db.execute(stmt)).scalars().all()
            for db_{{ cookiecutter.snake_name }} in db_{{ cookiecutter.snake_name }}s:
                db_{{ cookiecutter.snake_name }}.name = {{ cookiecutter.snake_name }}s_patch_request.name
            self.db.flush()
        return db_{{ cookiecutter.snake_name }}s

    async def delete_batch(self, ids: List[int]):
        async with self.db.begin():
            stmt_select = (await {{ cookiecutter.pascal_name }}.query()).filter({{ cookiecutter.pascal_name }}.id.in_(ids))
            db_{{ cookiecutter.snake_name }}s: List[{{ cookiecutter.pascal_name }}] = (await self.db.execute(stmt_select)).scalars().all()

            stmt_update = (
                update({{ cookiecutter.pascal_name }})
                .where({{ cookiecutter.pascal_name }}.deleted_at.is_(None))
                .filter({{ cookiecutter.pascal_name }}.id.in_(ids))
                .values(deleted_at=datetime.datetime.now())
            )
            await self.db.execute(stmt_update)
        return db_{{ cookiecutter.snake_name }}s

    async def get_by_id(self, {{ cookiecutter.snake_name }}_id: int) -> {{ cookiecutter.pascal_name }} | None:
        return await {{ cookiecutter.pascal_name }}.get_by(self.db, id={{ cookiecutter.snake_name }}_id)

    async def update_by_id(self, {{ cookiecutter.snake_name }}_id: int, {{ cookiecutter.snake_name }}_update_request: {{ cookiecutter.pascal_name }}UpdateRequest) -> {{ cookiecutter.pascal_name }} | None:
        async with self.db.begin():
            db_{{ cookiecutter.snake_name }}: {{ cookiecutter.pascal_name }} | None = await {{ cookiecutter.pascal_name }}.get_by(self.db, id={{ cookiecutter.snake_name }}_id)
            if db_{{ cookiecutter.snake_name }} is None:
                return None

            # 更新 name
            if {{ cookiecutter.snake_name }}_update_request.name is not None:
                db_{{ cookiecutter.snake_name }}.username = {{ cookiecutter.snake_name }}_update_request.name

            await db_{{ cookiecutter.snake_name }}.save(self.db)
        return db_{{ cookiecutter.snake_name }}

    async def delete_by_id(self, {{ cookiecutter.snake_name }}_id: int) -> {{ cookiecutter.pascal_name }} | None:
        async with self.db.begin():
            db_{{ cookiecutter.snake_name }}: {{ cookiecutter.pascal_name }} | None = await {{ cookiecutter.pascal_name }}.get_by(self.db, id={{ cookiecutter.snake_name }}_id)
            if db_{{ cookiecutter.snake_name }} is None:
                return None
            await db_{{ cookiecutter.snake_name }}.remove(self.db)
        return db_{{ cookiecutter.snake_name }}
