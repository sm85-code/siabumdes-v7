"""Alembic schema migration helpers."""
from __future__ import annotations

import asyncio
import os

from sqlalchemy import text

from app.core.database import SessionLocal


async def migrate_schema() -> None:
    from alembic import command
    from alembic.config import Config

    # alembic.ini stays at backend/alembic.ini for now
    config = Config(os.path.join(os.path.dirname(__file__), "..", "..", "..", "alembic.ini"))
    await asyncio.to_thread(command.upgrade, config, "head")


async def init_database() -> None:
    await migrate_schema()


async def applied_migrations() -> list[str]:
    async with SessionLocal() as session:
        rows = await session.execute(text("SELECT version_num FROM alembic_version ORDER BY version_num"))
        return [str(version) for version in rows.scalars()]
