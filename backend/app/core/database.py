"""SQLAlchemy async engine and session factory."""
from __future__ import annotations

import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


def _database_url() -> str:
    url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if not url:
        raise RuntimeError("DATABASE_URL wajib dikonfigurasi")
    parts = urlsplit(url)
    if parts.scheme not in {"postgresql", "postgres"}:
        raise RuntimeError("DATABASE_URL harus menggunakan PostgreSQL")
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k not in {"channel_binding", "sslmode"}]
    clean = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    return clean.replace("postgresql://", "postgresql+asyncpg://", 1).replace("postgres://", "postgresql+asyncpg://", 1)


class Base(DeclarativeBase):
    pass


_ssl_required = os.getenv("DATABASE_SSL", "require") != "disable"
engine = create_async_engine(
    _database_url(),
    connect_args={"ssl": "require" if _ssl_required else None, "timeout": 15},
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=15,
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def close_database() -> None:
    await engine.dispose()
