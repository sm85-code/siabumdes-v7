"""Shared MongoDB client for the FastAPI application."""
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URL, DB_NAME


_mongo_url = MONGO_URL
_db_name = DB_NAME
if not _mongo_url or not _db_name:
    raise RuntimeError("MONGO_URL dan DB_NAME wajib dikonfigurasi")

client = AsyncIOMotorClient(_mongo_url, serverSelectionTimeoutMS=5000)
db = client[_db_name]


async def close_database() -> None:
    client.close()
